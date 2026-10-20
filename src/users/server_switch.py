import glob
import os
import queue
import shutil
import subprocess
import threading
import socket
import time
from django.conf import settings


def restart_cp_self_command():
    try:
        subprocess.run("sudo systemctl restart cp", shell=True, check=True)
    except Exception as e:
        print(f"CP restart failed: {e}")
        
def restart_self():
    thread = threading.Thread(
        target=restart_cp_self_command,
        daemon=True  # 🔥 important
    )
    thread.start()

def get_web_service_name(server_type):
    

    os_name = getattr(settings, "MY_OS_NAME", "linux").strip().lower()
    server_type = (server_type or "").strip().lower()

    def service_exists(service):
        unit = f"{service}.service"

        result = subprocess.run(
            [
                "systemctl", "show",
                "-p", "LoadState", "--value",
                unit,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        load_state = result.stdout.strip()

        # A masked service exists, but cannot start until unmasked.
        if result.returncode == 0 and load_state in ("loaded", "masked"):
            return True

        # Fallback for installed unit files not currently loaded.
        return any(
            os.path.isfile(path)
            for path in (
                f"/etc/systemd/system/{unit}",
                f"/lib/systemd/system/{unit}",
                f"/usr/lib/systemd/system/{unit}",
            )
        )

    if server_type in ("ols", "openlitespeed", "lsws"):
        for service in ("lsws", "lshttpd"):
            if service_exists(service):
                return service

        raise ValueError(
            "OpenLiteSpeed service unit not found: lsws or lshttpd."
        )

    if server_type == "apache":
        services = (
            ("apache2", "httpd")
            if os_name in ("ubuntu", "debian")
            else ("httpd", "apache2")
        )

        for service in services:
            if service_exists(service):
                return service

        raise ValueError("Apache service not found: apache2 or httpd.")

    if server_type in ("nginx", "apache_nginx"):
        if service_exists("nginx"):
            return "nginx"

        raise ValueError("Nginx service not found.")

    if server_type == "apache_openlitespeed":
        raise ValueError(
            "apache_openlitespeed uses multiple web servers; "
            "it cannot be switched as a single service."
        )

    raise ValueError(f"Unsupported server type: {server_type}")


    


def switch_web_server_services(target_server_type, log):
    from users.server_core import get_server_type

    target_server_type = (target_server_type or "").strip().lower()
    current_server_type = get_server_type().strip().lower()

    if current_server_type == "ols":
        current_server_type = "openlitespeed"

    if target_server_type == "ols":
        target_server_type = "openlitespeed"

    current_service = get_web_service_name(current_server_type)
    target_service = get_web_service_name(target_server_type)

    if current_service == target_service:
        raise RuntimeError(
            "Current and target server resolved to the same systemd service."
        )

    def systemctl(*args, check=True):
        command = ["systemctl", *args]
        log("$ " + " ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        output = (result.stdout + result.stderr).strip()
        if output:
            log(output)

        if check and result.returncode != 0:
            raise RuntimeError(
                f"Command failed ({result.returncode}): "
                + " ".join(command)
            )

        return result

    def ports_are_free(ports=(80, 443)):
        """Check whether IPv4/IPv6 TCP ports can be bound."""
        for port in ports:
            for family, address in (
                (socket.AF_INET, ("0.0.0.0", port)),
                (socket.AF_INET6, ("::", port)),
            ):
                sock = socket.socket(family, socket.SOCK_STREAM)
                try:
                    if family == socket.AF_INET6:
                        sock.setsockopt(
                            socket.IPPROTO_IPV6,
                            socket.IPV6_V6ONLY,
                            1,
                        )
                    sock.bind(address)
                except OSError:
                    return False
                finally:
                    sock.close()

        return True

    

    was_active = subprocess.run(
        ["systemctl", "is-active", "--quiet", current_service],
        check=False,
    ).returncode == 0

    was_enabled = subprocess.run(
        ["systemctl", "is-enabled", "--quiet", current_service],
        check=False,
    ).returncode == 0

    log(f"Current service: {current_service}")
    log(f"Target service: {target_service}")
    # If the target service is already running, switching is complete.
    target_active = subprocess.run(
        ["systemctl", "is-active", "--quiet", target_service],
        check=False,
    ).returncode == 0

    if target_active:
        log(
            f"SUCCESS: Target service {target_service} is already active. "
            "No service changes are required."
        )
        return

    try:
        # Unmask the target before disrupting the current server.
        systemctl("unmask", target_service)

        # Stop and disable the old server.
        log(f"Stopping current server: {current_service}")
        systemctl("stop", current_service)

        log(f"Disabling current server: {current_service}")
        systemctl("disable", current_service)

        # Do not start the target while the old server still holds ports.
        wait_for_ports_free(timeout=15, log=log)

        log(f"Enabling target server: {target_service}")
        systemctl("enable", target_service)

        log(f"Starting target server: {target_service}")
        systemctl("start", target_service)

        active = subprocess.run(
            ["systemctl", "is-active", "--quiet", target_service],
            check=False,
        )

        if active.returncode != 0:
            raise RuntimeError(
                f"Target service {target_service} is not active."
            )

        log(f"SUCCESS: {target_service} is active and enabled.")

    except Exception:
        log("ERROR: Server switch failed; restoring the previous service.")

        systemctl("stop", target_service, check=False)

        if was_enabled:
            systemctl("enable", current_service, check=False)
        else:
            systemctl("disable", current_service, check=False)

        if was_active:
            systemctl("start", current_service, check=False)

        raise

def server_component_installed(component):
    if component == "apache":
        return bool(shutil.which("apache2ctl") or shutil.which("httpd"))

    if component == "ol_php":
        return any(
            os.path.isfile(path)
            for path in glob.glob("/opt/olspanel/ol-php*/root/bin/php")
        )

    if component == "repo":
        patterns = (
            "/etc/apt/sources.list.d/*olspanel*",
            "/etc/yum.repos.d/*olspanel*",
        )
        return any(
            glob.glob(pattern)
            for pattern in patterns
        )

    return False


def run_install_command(command, title, log):
    log(f"\n===== {title} =====")
    log(f"$ {command}")

    process = subprocess.Popen(
        ["bash", "-o", "pipefail", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    for line in iter(process.stdout.readline, ""):
        log(line.rstrip("\n"))

    process.stdout.close()
    return_code = process.wait()

    if return_code != 0:
        raise RuntimeError(
            f"{title} failed with exit code {return_code}"
        )

    log(f"===== {title}: completed =====")


def install_target_server(server_type, log):
    if server_type != "apache":
        return

    commands = []

    if not server_component_installed("repo"):
        commands.append((
            "curl -fsSL https://olspanel.com/repo-files/repo.sh | bash",
            "Configure OLSPanel repository",
        ))

    if not server_component_installed("ol_php"):
        commands.append((
            "curl -fsSL https://olspanel.com/extra/install_ol_php.sh | bash",
            "Install OLSPanel PHP",
        ))

    if not server_component_installed("apache"):
        commands.append((
            "curl -fsSL https://olspanel.com/extra/install-apache.sh | bash",
            "Install Apache",
        ))

    if not commands:
        log("Required components appear to be installed.")

    for command, title in commands:
        run_install_command(command, title, log)


def start_server_conversion(server_type, output_queue):
    if server_type == "apache":
        from users.server_core_apache import restart_openlitespeed
    else:
        from users.server_core_openlitespeed import restart_openlitespeed
    def log(message):
        output_queue.put(str(message))

    try:

        log(f"Starting conversion to {server_type}...")

        # Install required components and stream their output.
        install_target_server(server_type, log)
        if server_type != "openlitespeed" and not server_component_installed("ol_php"):
            raise RuntimeError(
                "This OS does not support multiple web servers "
                "because OLSPanel PHP is not installed or is not working. "
                "Server conversion has been stopped."
            )
        log("Converting domain configurations...")
        domain_result = convert_conf(server_type, log=log)

        if not domain_result.get("success"):
            raise RuntimeError("Domain configuration conversion failed.")

        log("Converting application configurations...")
        app_result = app_convert(server_type, log=log)

        if not app_result.get("success"):
            raise RuntimeError("Application configuration conversion failed.")
        #run_install_command(f"curl -sSL https://olspanel.com/extra/kill_port.sh | sudo bash -s -- 80 443", "Kill ports..", log)
        log("Switching web-server services...")
        switch_web_server_services(server_type, log)

        result = set_server_type(server_type)

        if str(result).startswith("Error:"):
            raise RuntimeError(result)
        run_install_command(f"curl -fsSL https://olspanel.com/extra/update-acme-reloadcmd.sh | bash -s -- {server_type}", "Updating acme..", log)
        log(f"Domains processed: {domain_result.get('total', 0)}")
        log(f"Apps processed: {app_result.get('total', 0)}")
        log(f"SUCCESS: Server type switched to {server_type}.")
        restart_openlitespeed()
        restart_self()

    except Exception as exc:
        log(f"ERROR: {exc}")

    finally:
        output_queue.put(None)


def server_conversion_stream(server_type):
    output_queue = queue.Queue()

    worker = threading.Thread(
        target=start_server_conversion,
        args=(server_type, output_queue),
        daemon=True,
    )
    worker.start()

    def generate():
        while True:
            message = output_queue.get()

            if message is None:
                yield "data: [DONE]\n\n"
                break

            for line in str(message).splitlines() or [""]:
                line = line.replace("\r", "")
                yield f"data: {line}\n"

            yield "\n"

    return generate()
    
    
def set_server_type(new_data):
   
    django_root = settings.BASE_DIR
    file_path = os.path.join(django_root, 'etc', 'server_type')
   
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            # Replace the file content
            with open(file_path, 'w') as f:
                f.write(new_data)
            return f"Success: File '{file_path}' content replaced."
        else:
            # Create the file and write the data
            os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
            with open(file_path, 'w') as f:
                f.write(new_data)
            return f"Success: File '{file_path}' created with new content."
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"


def convert_conf(SERVER_TYPE, log=None):
    from users.models import Domain

    if SERVER_TYPE == "apache":
        from users.server_core_apache import (
            normalize_domains,
            get_vhost_file,
            manage_listener_mapping,
            manage_ssl_listener_mapping,
            manage_virtual_host,
            create_vhost_file,
            replace_docroot_in_virtual_conf,
            change_php_version,
        )
    else:
        from users.server_core_openlitespeed import (
            normalize_domains,
            get_vhost_file,
            manage_listener_mapping,
            manage_ssl_listener_mapping,
            manage_virtual_host,
            create_vhost_file,
            replace_docroot_in_virtual_conf,
            change_php_version,
        )

    domains = Domain.objects.all()

    for index, domain_instance in enumerate(domains, start=1):
        domain_name = normalize_domains(domain_instance.domain.strip())

        if log:
            log(f"[DOMAIN {index}/{domains.count()}] Processing {domain_name}")

        username_string = str(domain_instance.userid)
        path = (domain_instance.path.replace(f'/home/{username_string}', '', 1).lstrip('/') or 'public_html')
        php_name = domain_instance.php or '8.2'

        new_php_version = php_name.replace('.', '')
        vhost_file = get_vhost_file(domain_name)

        if not os.path.exists(vhost_file):
            manage_listener_mapping("add", domain_name)
            manage_ssl_listener_mapping("add", domain_name)
            manage_virtual_host(domain_name, username_string)
            create_vhost_file(domain_name, username_string, path)
        else:
            replace_docroot_in_virtual_conf(vhost_file, domain_instance.path)

        change_php_version(
            domain_name,
            domain_name + new_php_version,
            new_php_version,
        )

        if log:
            log(f"[DOMAIN {index}/{domains.count()}] Completed {domain_name}")

    return {
        "success": True,
        "total": domains.count(),
        "message": "All domain configurations processed successfully.",
    }



    
    


def app_convert(SERVER_TYPE, log=None):
    from users.models import Apps, Domain

    if SERVER_TYPE == "apache":
        from users.server_core_apache import (
            create_ols_node_context,
            create_app_js,
            set_permissions_and_ownership,
        )
    else:
        from users.server_core_openlitespeed import (
            create_ols_node_context,
            create_app_js,
            set_permissions_and_ownership,
        )

    apps = Apps.objects.all()

    for index, app in enumerate(apps, start=1):
        domain = Domain.objects.filter(id=app.domain_id).first()

        if not domain:
            if log:
                log(f"[APP {index}/{apps.count()}] Skipping app {app.id}: domain not found")
            continue

        if log:
            log(f"[APP {index}/{apps.count()}] Processing {domain.domain}: {app.path}")

        domain_name = domain.domain
        username_string = str(domain.userid)
        app_path = app.path
        startup_file = app.startup_file
        app_version = app.version

        # Calculate the path relative to the domain document root.
        relative_path = app_path[len(domain.path):].lstrip('/')
        app_path_relative = relative_path or '/'

        if app.type == 'node_js':
            result = create_ols_node_context(app_version,app_path_relative,startup_file,domain_name)

            if not os.path.exists(os.path.join(app_path, startup_file)):
                create_app_js(app_path, startup_file)

        if log:
            log(f"[APP {index}/{apps.count()}] Completed {domain.domain}")

    return {
        "success": True,
        "total": apps.count(),
        "message": "All app configurations processed successfully.",
    }
    


def ports_are_free(ports=(80, 443)):
    """Return True if no TCP listener is using the specified ports."""
    result = subprocess.run(
        ["ss", "-H", "-ltn"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Could not check listening ports: {result.stderr.strip()}"
        )

    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) < 4:
            continue

        local_address = fields[3]
        port_text = local_address.rsplit(":", 1)[-1].rstrip("]")
        if port_text.isdigit() and int(port_text) in ports:
            return False

    return True


def wait_for_ports_free(timeout=15, log=None):
    def write_log(message):
        if log:
            log(message)

    # First wait for the current web server to release its ports.
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if ports_are_free():
            write_log("Ports 80 and 443 are available.")
            return

        time.sleep(0.5)

    # Run kill_port.sh only when an actual listener remains.
    write_log(
        "Ports 80/443 still have listeners. Running kill_port.sh..."
    )

    result = subprocess.run(
        [
            "bash",
            "-o",
            "pipefail",
            "-c",
            "curl -fsSL https://olspanel.com/extra/kill_port.sh "
            "| bash -s -- 80 443",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )

    output = (result.stdout + result.stderr).strip()
    if output:
        for line in output.splitlines():
            write_log(line)

    if result.returncode != 0:
        raise RuntimeError(
            f"kill_port.sh failed with exit code {result.returncode}."
        )

    # Verify actual listeners again after running the script.
    deadline = time.monotonic() + 10

    while time.monotonic() < deadline:
        if ports_are_free():
            write_log("Ports 80 and 443 are available.")
            return

        time.sleep(0.5)

    result = subprocess.run(
        ["ss", "-ltnp"],
        capture_output=True,
        text=True,
        check=False,
    )

    write_log("Remaining TCP listeners:")
    for line in result.stdout.splitlines():
        write_log(line)

    raise RuntimeError(
        "Ports 80/443 still have listeners after running kill_port.sh."
    )
