# yourapp/utils.py
import os
import subprocess
import re
import shutil
import stat
import pwd
import grp
import socket     
from datetime import datetime
from django.contrib import messages
import glob
from django.db import connection
from .models import * 
from .function import * 
from users.panellogger import *

from django.conf import settings
# Path to the OpenLiteSpeed configuration file for listeners
LISTENER_CONFIG_FILE = "/usr/local/lsws/conf/httpd_config.conf"
logger = CpLogger()

os_name = getattr(settings, "MY_OS_NAME", "linux").lower().strip()

if os_name in ["debian", "ubuntu", "mint"]:
    APACHE_CONFIG_PATH = "/etc/apache2"
    APACHE_CONFIG_FILE = f"{APACHE_CONFIG_PATH}/apache2.conf"
    APACHE_CONFIG_DIR = f"{APACHE_CONFIG_PATH}/conf-enabled"
    MODSECURITY_CONFIG_DIR = "/etc/modsecurity"
else:
    APACHE_CONFIG_PATH = "/etc/httpd/conf"
    APACHE_CONFIG_FILE = f"{APACHE_CONFIG_PATH}/httpd.conf"
    APACHE_CONFIG_DIR = "/etc/httpd/conf.d"
    MODSECURITY_CONFIG_DIR = "/etc/httpd/modsecurity.d"





def manage_listener_mapping(action, domain):
    return True



def manage_ssl_listener_mapping(action, domain):
    return True


def add_ipv6_ssl_listener():
    return True


def add_ipv6_panel_listener():
    return True


def preview_mapping(action, domain):
    return True



def ssl_preview_mapping(action, domain):
    return True


def manage_preview_virtual_host():
   
    config_file_path = "/usr/local/lsws/conf/httpd_config.conf"
    domain_name = "preview"
    vhost_directory = f"/usr/local/lsws/conf/vhosts/{domain_name}"
    vhost_file_path = os.path.join(vhost_directory, "vhconf.conf")
    if not os.path.isfile(vhost_file_path):
        create_preview_vhost_file()
    
    
    vhost_config = f"""
virtualhost preview {{
  vhRoot                  Example/
  configFile              conf/vhosts/preview/vhconf.conf
  allowSymbolLink         1
  enableScript            1
  restrained              1
}}
"""

    # Read the existing configuration to check for the virtual host
    try:
        with open(config_file_path, "r") as config_file:
            config_content = config_file.read()

            # Check if the virtual host block exists by looking for 'virtualhost <domain_name>'
            if f"virtualhost {domain_name} " in config_content:
                print(f"Virtual host for '{domain_name}' already exists.")  # Debug message
                return True  # Indicate that the virtual host already exists

    except FileNotFoundError:
        print("Configuration file does not exist.")  # Debug message
        return False  # Indicate failure
    except Exception as e:
        print(f"Error reading config file: {str(e)}")  # Debug message
        return False  # Indicate failure

    # If not found, append the new virtual host configuration
    try:
        with open(config_file_path, "a") as config_file:
            config_file.write(vhost_config.strip() + "\n")  # Ensure a new line at the end
            print(f"Added virtual host for '{domain_name}'.")  # Debug message
            return True  # Indicate success
    except Exception as e:
        print(f"Error writing to config file: {str(e)}")  # Debug message
        return False  # Indicate failure



def create_preview_vhost_file():
    """Create a vhost directory and configuration file for the specified domain."""
    domain_name = "preview"
    vhost_directory = f"/usr/local/lsws/conf/vhosts/{domain_name}"
    vhost_file_path = os.path.join(vhost_directory, "vhconf.conf")
    
    if not os.path.exists(vhost_directory):
        try:
            os.makedirs(vhost_directory)
            print(f"Created directory: {vhost_directory}")
        except Exception as e:
            print(f"Failed to create directory: {str(e)}")
            return False

    # Check if the vhost.conf file exists
    if not os.path.isfile(vhost_file_path):
        try:
            # Create the vhost.conf file with the specified content
            vhost_content = """docRoot                   $VH_ROOT/html/default
enableGzip                1

index  {
  useServer               0
  indexFiles              index.html
  autoIndex               0
  autoIndexURI            /_autoindex/default.php
}

errorpage 404 {
  url                     /error404.html
}

expires  {
  enableExpires           1
}

accessControl  {
  allow                   *
}

context / {
  location                $DOC_ROOT/
  allowBrowse             1

  rewrite  {
    RewriteFile .htaccess
  }
}

rewrite  {
  enable                  0
  logLevel                0
}

scripthandler  {
  add                     lsapi:lsphp lsphp
}

"""
            with open(vhost_file_path, "w") as vhost_file:
                vhost_file.write(vhost_content)

            print(f"Created vhost file: {vhost_file_path}")
            return True
        except Exception as e:
            print(f"Failed to create vhost file: {str(e)}")
            return False
    else:
        print(f"Vhost file '{vhost_file_path}' already exists.")
        return False


def update_context_block(context_name, path):
    vhost_directory = "/usr/local/lsws/conf/vhosts/preview"
    conf_path = os.path.join(vhost_directory, "vhconf.conf")
    name, block = get_single_extprocessor_block(context_name)
    php_preview_mapping(name)
    context_header = f"context /~{context_name} {{"
    context_footer = "}"
    name_header = f"extprocessor {name} {{"

    new_block = f"""{context_header}
  location                {path}
  allowBrowse             1
  indexFiles              index.php, index.html
  
  accessControl  {{
    allow                 *
  }}

  rewrite  {{
  enable                  1
  autoLoadHtaccess        1
  RewriteRule ^.*\.php$ - [H=application/x-httpd-{name}]
  }}

  addDefaultCharset       off

  phpIniOverride  {{
    php_admin_value open_basedir "/tmp:{path}"
  }}
{context_footer}
"""

    try:
        # Read current file if exists
        if os.path.exists(conf_path):
            with open(conf_path, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        # Remove old context block
        inside_block = False
        new_lines = []
        for line in lines:
            if line.strip().startswith(context_header):
                inside_block = True
                continue
            if inside_block and line.strip() == context_footer:
                inside_block = False
                continue
            if not inside_block:
                new_lines.append(line)

        # Remove old extprocessor block
        lines = new_lines
        inside_block = False
        final_lines = []
        for line in lines:
            if line.strip().startswith(name_header):
                inside_block = True
                continue
            if inside_block and line.strip() == context_footer:
                inside_block = False
                continue
            if not inside_block:
                final_lines.append(line)

        # Combine everything
        updated_content = "".join(final_lines).rstrip() + "\n\n" + new_block + "\n\n" + block

        # Write back to file
        with open(conf_path, "w") as f:
            f.write(updated_content)
           

        print(f"Updated context and extprocessor for /{context_name} in {conf_path}")
        return True

    except Exception as e:
        print(f"Error updating context: {str(e)}")
        return False


def get_single_extprocessor_block(domain_name):
    vhost_directory = f"/usr/local/lsws/conf/vhosts/{domain_name}" 
    vhost_file_path = os.path.join(vhost_directory, "vhost.conf")
    if not os.path.isfile(vhost_file_path):
        print(f"File not found: {vhost_file_path}")
        return None, None

    with open(vhost_file_path, "r") as f:
        content = f.read()

    match = re.search(r"extprocessor\s+(\S+)\s*\{.*?\n\}", content, re.DOTALL)
    if match:
        name = match.group(1)
        block = match.group(0).strip()
        return name, block

    return None, None



def php_preview_mapping(name):
    vhost_directory = "/usr/local/lsws/conf/vhosts/preview"
    conf_path = os.path.join(vhost_directory, "vhconf.conf")
    action = "add"

    try:
        with open(conf_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        in_listener_block = False
        mapping_found = False

        for line in lines:
            if 'scripthandler  {' in line:
                in_listener_block = True

            # Adjust the map line format to remove extra spaces
            if in_listener_block:
                
                if action == "add" and f"  add                     lsapi:{name} {name}" in line:
                    mapping_found = True
                    

            new_lines.append(line)

            if '}' in line and in_listener_block:
                # Add the map if it's not found for 'add' action
                if action == "add" and not mapping_found:
                    new_lines.insert(-1, f"  add                     lsapi:{name} {name}\n")
                in_listener_block = False

        # Write the modified lines back to the configuration file
        with open(conf_path, 'w') as file:
            file.writelines(new_lines)

        
        return True

    except Exception as e:
        print(f"Error updating scripthandler mapping: {e}")
        return False

        
def panel_listener_mapping(action, domain):
    binary_path = "/usr/local/bin/olspanelcp"

    # 🚫 If OLS Panel binary exists → skip everything
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        print("OLS Panel binary found — skipping IPv6 listener setup.")
        return
    try:
        with open(LISTENER_CONFIG_FILE, 'r') as file:
            lines = file.readlines()

        new_lines = []
        in_listener_block = False
        mapping_found = False

        for line in lines:
            if 'listener panel {' in line:
                in_listener_block = True

            # Adjust the map line format to remove extra spaces
            if in_listener_block:
                if action == "remove" and f"  map                     panel_{domain} " in line:
                    mapping_found = True
                    continue

                if action == "add" and f"  map                     panel_{domain} " in line:
                    mapping_found = True
                    

            new_lines.append(line)

            if '}' in line and in_listener_block:
                # Add the map if it's not found for 'add' action
                if action == "add" and not mapping_found:
                    new_lines.insert(-1, f"  map                     panel_{domain} {domain}\n")
                in_listener_block = False

        # Write the modified lines back to the configuration file
        with open(LISTENER_CONFIG_FILE, 'w') as file:
            file.writelines(new_lines)

        print(f"Mapping for '{domain}' {'added' if action == 'add' else 'removed'} successfully.")
        return True

    except Exception as e:
        print(f"Error managing SSL listener mapping: {e}")
        return False


    except Exception as e:
        print(f"Error managing listener mapping: {e}")
        return False



def panel_virtual_host(domain_name):
    binary_path = "/usr/local/bin/olspanelcp"

    # 🚫 If OLS Panel binary exists → skip everything
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        print("OLS Panel binary found — skipping IPv6 listener setup.")
        return
    
    
    """Check if the virtual host exists, and add it if not."""
    config_file_path = "/usr/local/lsws/conf/httpd_config.conf"
    
    # Define the virtual host configuration block
    vhost_config = f"""
virtualhost panel_{domain_name} {{
  vhRoot                  Example/
  configFile              $SERVER_ROOT/conf/vhosts/$VH_NAME/vhost.conf
  allowSymbolLink         1
  enableScript            1
  restrained              1
  setUIDMode              0
}}
"""

    # Read the existing configuration to check for the virtual host
    try:
        with open(config_file_path, "r") as config_file:
            config_content = config_file.read()

            # Check if the virtual host block exists by looking for 'virtualhost <domain_name>'
            if f"virtualhost panel_{domain_name} " in config_content:
                print(f"Virtual host for '{domain_name}' already exists.")  # Debug message
                return True  # Indicate that the virtual host already exists

    except FileNotFoundError:
        print("Configuration file does not exist.")  # Debug message
        return False  # Indicate failure
    except Exception as e:
        print(f"Error reading config file: {str(e)}")  # Debug message
        return False  # Indicate failure

    # If not found, append the new virtual host configuration
    try:
        with open(config_file_path, "a") as config_file:
            config_file.write(vhost_config.strip() + "\n")  # Ensure a new line at the end
            print(f"Added virtual host for '{domain_name}'.")  # Debug message
            return True  # Indicate success
    except Exception as e:
        print(f"Error writing to config file: {str(e)}")  # Debug message
        return False  # Indicate failure
        

def create_panel_vhost_file(domain_name):
    binary_path = "/usr/local/bin/olspanelcp"

    # 🚫 If OLS Panel binary exists → skip everything
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        print("OLS Panel binary found — skipping IPv6 listener setup.")
        return
    # Paths
    template_path = "/usr/local/lsws/conf/vhosts/mypanel/vhconf.conf"
    vhost_directory = f"/usr/local/lsws/conf/vhosts/panel_{domain_name}"
    vhost_file_path = os.path.join(vhost_directory, "vhost.conf")
    
    

    # Create vhost directory if not exists
    if not os.path.exists(vhost_directory):
        try:
            os.makedirs(vhost_directory)
            print(f"Created directory: {vhost_directory}")
        except Exception as e:
            print(f"Failed to create vhost directory: {str(e)}")
            return False

    # Read template and replace cert lines
    try:
        with open(template_path, 'r') as template_file:
            content = template_file.readlines()

        new_content = []
        for line in content:
            if "keyFile" in line:
                new_content.append(f"  keyFile                 /etc/letsencrypt/live/{domain_name}/privkey.pem\n")
            elif "certFile" in line:
                new_content.append(f"  certFile                /etc/letsencrypt/live/{domain_name}/fullchain.pem\n")
            else:
                new_content.append(line)

        with open(vhost_file_path, 'w') as new_file:
            new_file.writelines(new_content)
            print(f"Created vhost config: {vhost_file_path}")

        return True

    except Exception as e:
        print(f"Error copying or modifying vhost file: {str(e)}")
        return False
    
def get_all_panel_domains_and_create_vhosts():
    binary_path = "/usr/local/bin/olspanelcp"

    # 🚫 If OLS Panel binary exists → skip everything
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        print("OLS Panel binary found — skipping IPv6 listener setup.")
        return
        
    base_path = "/usr/local/lsws/conf/vhosts"
    try:
        with os.scandir(base_path) as entries:
            for entry in entries:
                if entry.is_dir() and entry.name.startswith("panel_"):
                    domain = entry.name.replace("panel_", "", 1)
                    create_panel_vhost_file(domain)  # Call your function
    except Exception as e:
        print(f"Error: {e}")

def create_self_signed_ssl(domain, base_ssl_dir="/etc/letsencrypt/live"):
    """
    Create a self-signed SSL certificate for a given domain and store it in the specified SSL directory.

    Args:
        domain (str): The domain for which the SSL certificate is generated.
        base_ssl_dir (str): The base directory for storing SSL certificates (default: /etc/letsencrypt/live).

    Returns:
        dict: Paths to the private key and certificate files if successful, None otherwise.
    """
    try:
        # Define the full paths for the private key and certificate
        private_key_path = f"{base_ssl_dir}/{domain}/privkey.pem"
        certificate_path = f"{base_ssl_dir}/{domain}/fullchain.pem"
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
        
        # Generate the private key
        subprocess.run(["openssl", "genrsa", "-out", private_key_path, "2048"], check=True)
        
        # Generate the certificate signing request (CSR)
        subprocess.run([
            "openssl", "req", "-new", "-key", private_key_path, "-out", "/tmp/csr.pem",
            "-subj", f"/CN={domain}/O=My Pannel/C=US"  # Update this subject line as needed
        ], check=True)
        
        # Generate the self-signed certificate (valid for 365 days)
        subprocess.run([
            "openssl", "x509", "-req", "-days", "365", "-in", "/tmp/csr.pem", "-signkey", private_key_path, "-out", certificate_path
        ], check=True)
        
        # Clean up the CSR file
        os.remove("/tmp/csr.pem")
        
        print(f"SSL certificate created successfully for {domain}.")
        print(f"Private Key File: {private_key_path}")
        print(f"Certificate File: {certificate_path}")
        print("Chained Certificate: Yes")
        
        return {
            "private_key": private_key_path,
            "certificate": certificate_path,
            "chained": True
        }
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating SSL certificate: {e}")
        return None

# Usage example:
# create_self_signed_ssl('ols-example.tk')


def manage_virtual_host(domain_name, username):
    
    return True  # Indicate failure






def create_vhost_file(domain_name, username, document_root="public_html"):
    """
    Create Apache VirtualHost and PHP-FPM configuration.
    """

    apache_conf_directory = APACHE_CONFIG_DIR
    apache_conf_file = f"{apache_conf_directory}/{domain_name}.conf"
    document_root_path = f"/home/{username}/{document_root}"
    log_directory = f"/home/{username}/logs"
    php_version = "8.3"
    cache_directory = f"/home/{username}/cache/{domain_name}" 
    php_version_number = re.sub(r"\D", "", str(php_version))
    php_socket = f"/run/olspanel/ol-php{php_version_number}/{domain_name.replace('.', '_')}{php_version_number}.sock"
    ssl_certificate = f"/etc/letsencrypt/live/{domain_name}/fullchain.pem"
    ssl_certificate_key = f"/etc/letsencrypt/live/{domain_name}/privkey.pem"

    try:
        os.makedirs(log_directory, exist_ok=True)
        os.makedirs(apache_conf_directory, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directories: {e}")
        return False

    if os.path.isfile(apache_conf_file):
        print(f"Apache vhost already exists: {apache_conf_file}")
        return False

    apache_config = f"""<VirtualHost *:80>
    ServerName {domain_name}
    ServerAlias www.{domain_name}
    DocumentRoot {document_root_path}

    <Directory {document_root_path}>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    DirectoryIndex index.php index.html

    <IfModule proxy_fcgi_module>
        <FilesMatch \\.php$>
            SetHandler proxy:unix:{php_socket}|fcgi://{domain_name}
        </FilesMatch>
    </IfModule>
    <IfModule mod_cache.c>
        <IfModule mod_cache_disk.c>
	        CacheRoot "{cache_directory}"
            CacheEnable disk /
        </IfModule>
    </IfModule>
    ErrorLog {log_directory}/{domain_name}.error_log
    CustomLog {log_directory}/{domain_name}.access_log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName {domain_name}
    ServerAlias www.{domain_name}
    DocumentRoot {document_root_path}

    <Directory {document_root_path}>
        Options FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    DirectoryIndex index.php index.html

    SSLEngine On
    SSLCertificateFile {ssl_certificate}
    SSLCertificateKeyFile {ssl_certificate_key}

    <IfModule proxy_fcgi_module>
        <FilesMatch \\.php$>
            SetHandler proxy:unix:{php_socket}|fcgi://{domain_name}
        </FilesMatch>
    </IfModule>
    <IfModule mod_cache.c>
        <IfModule mod_cache_disk.c>
	        CacheRoot "{cache_directory}"
            CacheEnable disk /
        </IfModule>
    </IfModule>
    ErrorLog {log_directory}/{domain_name}-ssl-error.log
    CustomLog {log_directory}/{domain_name}-ssl-access.log combined
</VirtualHost>
"""

    try:
        with open(apache_conf_file, "w") as apache_file:
            apache_file.write(apache_config)

        print(f"Created Apache vhost: {apache_conf_file}")

    except Exception as e:
        print(f"Failed to create Apache vhost: {e}")
        return False

    # Create PHP-FPM pool configuration
    if not create_fpm_conf(domain_name, username, php_version,document_root):
        print("Failed to create PHP-FPM configuration.")

        try:
            os.remove(apache_conf_file)
        except Exception:
            pass

        return False

    try:
        test_result = subprocess.run(
            ["sudo", "apachectl", "-t"],
            capture_output=True,
            text=True
        )

        if test_result.returncode != 0:
            print("Apache configuration test FAILED:")
            print(test_result.stdout)
            print(test_result.stderr)

            try:
                print("Apache configuration test FAILED:")
                #os.remove(apache_conf_file)
            except Exception:
                pass

            return False

        print("Apache configuration test passed.")

    except Exception as e:
        print(f"Failed to test Apache configuration: {e}")
        return False

    try:
        reload_openlitespeed()

        print("Apache reloaded successfully.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Failed to reload Apache: {e}")
        return False

    except Exception as e:
        print(f"Apache reload error: {e}")
        return False
        
  
def find_fpm_username(domain_name):
  try:
    pattern = re.compile(r"^\s*user\s*=\s*([^\s#]+)", re.MULTILINE)

    # Normalize name variations: panel_fsb_bd -> panel.fsb.bd
    normalized_name = domain_name.replace("_", ".")

    # Match all PHP version directories (ol-php82, ol-php83, etc.)
    php_dirs = sorted(glob.glob("/opt/olspanel/ol-php*/root/etc/php-fpm.d"))

    for php_dir in php_dirs:
      # Check potential filename variations
      possible_files = [
          os.path.join(php_dir, f"{domain_name}.conf"),
          os.path.join(php_dir, f"{normalized_name}.conf"),
      ]

      conf_file = None
      for target in possible_files:
        if os.path.isfile(target):
          conf_file = target
          break

      # If named file isn't found, search all .conf files in the directory
      if not conf_file:
        for file in glob.glob(os.path.join(php_dir, "*.conf")):
          if (
              domain_name in os.path.basename(file)
              or normalized_name in os.path.basename(file)
          ):
            conf_file = file
            break

      if not conf_file or not os.path.isfile(conf_file):
        continue

      try:
        with open(conf_file, "r") as file:
          content = file.read()

        match = pattern.search(content)

        if match:
          username = match.group(1).strip()
          if username:
            print(f"Found FPM username for {domain_name}: {username}")
            print(f"FPM config: {conf_file}")
            return username

      except Exception as e:
        print(f"Error reading {conf_file}: {e}")

    print(f"No FPM configuration found for domain: {domain_name}")
    return None

  except Exception as e:
    print(f"Error searching FPM configurations: {e}")
    return None

  
def create_fpm_conf(domain_name, username, php_version, document_root="public_html"):
    try:
        version_number = re.sub(r"\D", "", str(php_version))
        if not version_number:
            print(f"Invalid PHP version: {php_version}")
            return False

        php_dir = f"/opt/olspanel/ol-php{version_number}/root"
        fpm_dir = f"{php_dir}/etc/php-fpm.d"
        conf_file = f"{fpm_dir}/{domain_name}.conf"

        pool_name = domain_name.replace(".", "_")
        socket_name = f"{pool_name}{version_number}"
        socket_path = f"/run/olspanel/ol-php{version_number}/{socket_name}.sock"

        username = str(username or "").strip()

        if not username:
            username = find_fpm_username(domain_name) or ""
            if username:
                print(f"FPM username found from another PHP version: {username}")

        if not username:
            print(f"PHP-FPM username is empty for {domain_name}.")
            return False

        document_root_path = f"/home/{username}/{document_root}"
        log_directory = f"/home/{username}/logs"
        log_path = f"{log_directory}/{domain_name}.php.error.log"

        open_basedir = (
            f"home/{username}:"
            f"/home/{username}:"
            f"/tmp:"
            f"/usr/share/php:"
            f"/opt/olspanel/ol-php{version_number}/root"
        )

        os.makedirs(fpm_dir, exist_ok=True)
        os.makedirs(os.path.dirname(socket_path), exist_ok=True)
        os.makedirs(log_directory, exist_ok=True)

        config = f"""[{pool_name}]
user = {username}
group = {username}
chdir = /home/{username}
catch_workers_output = yes
listen = {socket_path}
listen.owner = {username}
listen.group = nogroup
listen.mode = 0660
pm = ondemand
pm.max_children = 50
pm.max_requests = 900
pm.process_idle_timeout = 100
php_admin_flag[allow_url_fopen] = on
php_admin_flag[log_errors] = on
php_admin_value[disable_functions] = exec,passthru,shell_exec,system
php_admin_value[short_open_tag] = on
php_admin_value[open_basedir] = {open_basedir}
php_value[doc_root] = ""
php_value[error_log] = {log_path}
php_value[error_reporting] = E_ALL & ~E_NOTICE
ping.path = /ping
pm.status_path = /status
security.limit_extensions = .phtml .php .php3 .php4 .php5 .php6 .php7 .php8
"""

        with open(conf_file, "w") as file:
            file.write(config)

        print(f"PHP-FPM configuration created: {conf_file}")
        print(f"PHP-FPM socket: {socket_path}")
        print(f"PHP-FPM user: {username}")
        print(f"open_basedir: {open_basedir}")

        return True

    except Exception as e:
        print(f"Error creating PHP-FPM configuration: {e}")
        return False       
        



def clean_conf_file_path(conf_file_path):
  """Strips trailing '/vhost.conf' or '.vhost.conf' and ensures the path ends with '.conf'."""
  # If path ends with /vhost.conf (e.g., /path/to/domain/vhost.conf -> /path/to/domain.conf)
  if conf_file_path.endswith("/vhost.conf"):
    conf_file_path = conf_file_path[:-11] + ".conf"
  # If path ends with .vhost.conf (e.g., /path/to/domain.vhost.conf -> /path/to/domain.conf)
  elif conf_file_path.endswith(".vhost.conf"):
    conf_file_path = conf_file_path[:-11] + ".conf"

  return conf_file_path        

def replace_docroot_in_virtual_conf(conf_file_path, new_docroot_path):
  # Sanitize configuration file path
  conf_file_path = clean_conf_file_path(conf_file_path)

  if not os.path.isfile(conf_file_path):
    print(f"Configuration file {conf_file_path} not found.")
    return False

  try:
    new_docroot_path = new_docroot_path.rstrip("/")

    with open(conf_file_path, "r") as file:
      content = file.read()

    # 1. Replace ALL DocumentRoot lines (removed count=1)
    content, docroot_count = re.subn(
        r"^(\s*)DocumentRoot\s+.*$",
        rf"\1DocumentRoot {new_docroot_path}",
        content,
        flags=re.MULTILINE,
    )

    if docroot_count == 0:
      print(f"DocumentRoot not found in {conf_file_path}.")
      return False

    # 2. Replace ALL <Directory ...> paths (removed count=1)
    content, directory_count = re.subn(
        r"^(\s*<Directory\s+)[^>]+(>)",
        rf"\1{new_docroot_path}\2",
        content,
        flags=re.MULTILINE,
    )

    with open(conf_file_path, "w") as file:
      file.write(content)

    print(
        f"Successfully updated {docroot_count} DocumentRoot line(s) and"
        f" {directory_count} <Directory> block(s) to '{new_docroot_path}' in"
        f" {conf_file_path}."
    )

    return True

  except Exception as e:
    print(f"An error occurred: {e}")
    return False
        
def remove_map_from_httpd_config(domain_name):
   
    return True
        
def remove_virtual_host_from_httpd_config(domain_name):
    return True
        
def remove_domain_folder(domain_name):
    """
    Remove the Apache vhost configuration for a domain.
    """

    conf_file = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    if os.path.isfile(conf_file):
        try:
            os.remove(conf_file)

            return (
                f"Domain configuration '{conf_file}' "
                f"removed successfully."
            )

        except Exception as e:
            return (
                f"An error occurred while removing "
                f"the configuration: {e}"
            )

    else:
        return (
            f"Domain configuration '{conf_file}' "
            f"does not exist."
        )


def add_user_and_set_folder_permissions(username, home_dir, full_path, groupname=None):
    # Use username as groupname if not provided
    if groupname is None:
        groupname = username

    # Step 1: Check if the group exists; create it if not
    try:
        grp.getgrnam(groupname)
        logger.error(f"Group {groupname} already exists.")
    except KeyError:
        # Create the group
        try:
            subprocess.run(['sudo', 'groupadd', groupname], check=True)
            print(f"Group {groupname} added successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error adding group {groupname}: {e}")
            return False

    # Step 2: Check if the user exists; create it if not
    try:
        pwd.getpwnam(username)
        print(f"User {username} already exists.")
    except KeyError:
        # Add the user and assign it to the group
        try:
            if getattr(settings, "MY_OS_NAME", "linux") == "ubuntu":
                subprocess.run(['sudo', 'adduser', '--disabled-password', '--gecos', '', '--ingroup', groupname, username], check=True)
                
            else:
                subprocess.run(['sudo', 'useradd',  '-g', groupname, '-m', username], check=True)
                
            
            print(f"User {username} added successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error adding user {username}: {e}")
            return False

    # Step 3: Create the home directory if it does not exist
    try:
        os.makedirs(home_dir, exist_ok=True)  # Create home directory if it does not exist
        print(f"Created home directory: {home_dir}")
    except Exception as e:
        logger.error(f"Error creating home directory {home_dir}: {e}")
        return False

    # Step 4: Set home directory permissions to 711
    try:
        os.chmod(home_dir, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)  # 711 (rwx--x--x)
        print(f"Permissions for {home_dir} set to 711.")
    except Exception as e:
        logger.error(f"Error setting permissions for {home_dir}: {e}")
        return False

    # Step 5: Create the document root directory if it does not exist
    try:
        os.makedirs(full_path, exist_ok=True)  # Create the directory and any necessary parent directories
        print(f"Created directory: {full_path}")
    except Exception as e:
        logger.error(f"Error creating directory {full_path}: {e}")
        return False

    # Step 6: Set ownership for the created home directory
    try:
        os.chown(home_dir, pwd.getpwnam(username).pw_uid, grp.getgrnam(groupname).gr_gid)
        print(f"Ownership for {home_dir} set to {username}:{groupname}.")
    except Exception as e:
        logger.error(f"Error setting ownership for {home_dir}: {e}")
        return False

    # Step 7: Set ownership for the created document root directory
    try:
        os.chown(full_path, pwd.getpwnam(username).pw_uid, grp.getgrnam(groupname).gr_gid)
        print(f"Ownership for {full_path} set to {username}:{groupname}.")
    except Exception as e:
        logger.error(f"Error setting ownership for {full_path}: {e}")
        return False

    # Step 8: Set permissions for the created document root directory to 755
    try:
        os.chmod(full_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)  # 755 (rwxr-xr-x)
        print(f"Permissions for {full_path} set to 755.")
    except Exception as e:
        logger.error(f"Error setting permissions for {full_path}: {e}")
        return False

    # Step 9: Ensure the "nobody" group and user exist
    try:
        grp.getgrnam('nobody')
        print("Group 'nobody' already exists.")
    except KeyError:
        # Create the group 'nobody' if it doesn't exist
        try:
            subprocess.run(['sudo', 'groupadd', 'nobody'], check=True)
            print("Group 'nobody' created successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating group 'nobody': {e}")
            return False

    try:
        pwd.getpwnam('nobody')
        print("User 'nobody' already exists.")
    except KeyError:
        # Create the user 'nobody' as a system user with no login shell
        try:
            subprocess.run(['sudo', 'useradd', '-r', '-s', '/usr/sbin/nologin', '-g', 'nobody', 'nobody'], check=True)
            print("User 'nobody' created successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating user 'nobody': {e}")
            return False

    # Step 10: Modify the full path ownership and permissions
    try:
        # Change ownership to 'username:nobody'
        subprocess.run(['sudo', 'chown', '-R', f'{username}:nobody', full_path], check=True)
        print(f"Ownership for {full_path} set to {username}:nobody.")

        # Change permissions to 775
        subprocess.run(['sudo', 'chmod', '-R', '775', full_path], check=True)
        print(f"Permissions for {full_path} set to 775.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting ownership/permissions for {full_path}: {e}")
        return False

    return True
    
def set_permissions_and_ownership(path, username, groupname=None, permissions=None):
    
    if groupname is None:
        groupname = username

    # Validate user and group
    try:
        user_info = pwd.getpwnam(username)
        group_info = grp.getgrnam(groupname)
    except KeyError as e:
        logger.error(e)
        print(f"Error: {e}")
        return False

    def apply_recursively(target_path):
        """
        Applies ownership and permissions to the target path and its contents if it's a directory.
        """
        try:
            # Set ownership
            os.chown(target_path, user_info.pw_uid, group_info.gr_gid)
            print(f"Ownership set for {target_path} to {username}:{groupname}.")

            # Determine and set permissions
            if permissions is None:
                if os.path.isdir(target_path):
                    path_permissions = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH  # 755
                else:
                    path_permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH  # 644
            else:
                path_permissions = permissions

            os.chmod(target_path, path_permissions)
            print(f"Permissions set for {target_path} to {oct(path_permissions)}.")

            # If it's a directory, recursively apply to contents
            if os.path.isdir(target_path):
                for entry in os.scandir(target_path):
                    apply_recursively(entry.path)
        except Exception as e:
            print(f"Error applying ownership or permissions for {target_path}: {e}")
            return False

    # Start the process for the given path
    apply_recursively(path)
    return True

    
def restart_openlitespeed():
    os_name = getattr(settings, "MY_OS_NAME", "linux").strip().lower()

    if os_name in ("ubuntu", "debian", "linux mint"):
        service_name = "apache2"
    else:
        service_name = "httpd"

    try:
        subprocess.run(
            ["sudo", "systemctl", "restart", service_name],
            check=True
        )
        print("Apache has been restarted successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Apache: {e}")

    finally:
        try:
            restart_lsphp()
        except Exception as e:
            print(f"Failed to restart PHP-FPM services: {e}")
            

def get_php_versions():
    php_versions = []

    # Define a regex pattern to match version numbers
    version_pattern = re.compile(r'^\d+(\.\d+)?$')

    base_directory = '/opt/olspanel'

    if not os.path.isdir(base_directory):
        return php_versions

    # Get all directories starting with 'ol-php'
    for filename in os.listdir(base_directory):

        if filename.startswith('ol-php'):
            # Extract the version
            version = filename.replace('ol-php', '', 1)

            # Check if the extracted version matches
            # versions like 8.3, 8.4, 8.5, 8.6
            if version_pattern.match(version):

                # Add a dot after the first digit
                # Example: 83 -> 8.3
                if '.' not in version:
                    version = f"{version[0]}.{version[1:]}"

                php_versions.append(version)

    # Sort versions numerically
    php_versions.sort(
        key=lambda x: list(map(int, x.split('.')))
    )

    return php_versions
    
    
def replace_php_version_in_vhost(domain_name, new_php_version):
    vhost_file_path = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    try:
        if not os.path.isfile(vhost_file_path):
            return f"ERROR: File not found: {vhost_file_path}"

        version_number = re.sub(r"\D", "", str(new_php_version).strip())

        if not version_number:
            return f"ERROR: Invalid PHP version: {new_php_version}"

        with open(vhost_file_path, "r") as file:
            content = file.read()

        pattern = re.compile(
            r"/run/olspanel/ol-php\d+/([^/\s|]+\.sock)"
        )

        updated_content, count = pattern.subn(
            lambda match: (
                f"/run/olspanel/ol-php{version_number}/"
                + re.sub(
                    r"\d+\.sock$",
                    f"{version_number}.sock",
                    match.group(1),
                )
            ),
            content,
        )

        if count == 0:
            return f"ERROR: No matching PHP socket found in {vhost_file_path}"

        if updated_content == content:
            return f"INFO: Socket already uses PHP {version_number}: {vhost_file_path}"

        with open(vhost_file_path, "w") as file:
            file.write(updated_content)

        return (
            f"SUCCESS: Updated {vhost_file_path}; "
            f"PHP socket changed to PHP {version_number}. "
            f"Matches: {count}"
        )

    except Exception as e:
        return f"ERROR: {e}"



def replace_extprocessor_socket_and_path(domain_name, new_processor_name, pure_version):
    vhost_file_path = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    try:
        if not os.path.isfile(vhost_file_path):
            print(f"Configuration file {vhost_file_path} does not exist.")
            return False

        pure_version = str(pure_version).strip()
        version_number = pure_version.replace(".", "")

        if not version_number.isdigit():
            print(f"Invalid PHP version: {pure_version}")
            return False

        with open(vhost_file_path, "r") as file:
            content = file.read()

        pattern = re.compile(
            r"/run/olspanel/ol-php[^/\s|]+/([^/\s|]+\.sock)"
        )

        matches = pattern.findall(content)

        if not matches:
            print(f"No PHP-FPM socket found in {vhost_file_path}.")
            return False

        for socket_filename in matches:
            new_socket_filename = re.sub(
                r"\d+\.sock$",
                f"{version_number}.sock",
                socket_filename
            )

            old_pattern = re.compile(
                r"/run/olspanel/ol-php[^/\s|]+/"
                + re.escape(socket_filename)
            )

            new_socket = (
                f"/run/olspanel/ol-php{version_number}/"
                f"{new_socket_filename}"
            )

            content = old_pattern.sub(
                new_socket,
                content
            )

            print(
                f"Replaced PHP-FPM socket: "
                f"{socket_filename} -> {new_socket}"
            )

        with open(vhost_file_path, "w") as file:
            file.write(content)

        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False




def replace_path(domain_name, pure_version):
    vhost_file_path = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    if not os.path.isfile(vhost_file_path):
        print(f"File not found: {vhost_file_path}")
        return False

    try:
        pure_version = str(pure_version).strip()
        version_number = pure_version.replace(".", "")

        if not version_number.isdigit():
            print(f"Invalid PHP version: {pure_version}")
            return False

        with open(vhost_file_path, "r") as file:
            content = file.read()

        socket_pattern = re.compile(
            r"/run/olspanel/ol-php[^/\s|]+/([^/\s|]+\.sock)"
        )

        matches = socket_pattern.findall(content)

        if not matches:
            print(f"No PHP-FPM socket found in {vhost_file_path}")
            return False

        for socket_filename in matches:
            new_socket_filename = re.sub(
                r"\d+\.sock$",
                f"{version_number}.sock",
                socket_filename
            )

            old_socket = re.search(
                r"/run/olspanel/ol-php[^/\s|]+/"
                + re.escape(socket_filename),
                content
            )

            if old_socket:
                new_socket = (
                    f"/run/olspanel/ol-php{version_number}/"
                    f"{new_socket_filename}"
                )

                content = content.replace(
                    old_socket.group(0),
                    new_socket
                )

                print(
                    f"Replaced PHP-FPM socket: "
                    f"{old_socket.group(0)} -> {new_socket}"
                )

        with open(vhost_file_path, "w") as file:
            file.write(content)

        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    
def change_php_version(domain_name, version_name, version):
    from users.models import Domain    
    version_name = str(version_name).replace('.', '')
    version = str(version).strip()

    replace_php_version_in_vhost(domain_name,version)
    replace_path(domain_name,version)
    create_fpm_conf(domain_name, "", version)
    replace_extprocessor_socket_and_path(domain_name,f"ol-php{version_name}",version)
    domain_s = Domain.objects.filter(domain=domain_name).first()
    username = domain_s.userid
    cache_directory = f"/home/{username}/cache/{domain_name}"
    create_cache_directory(cache_directory)

    return True

def create_cache_directory(cache_directory):
    try:
        os.makedirs(cache_directory, exist_ok=True)
        subprocess.run(["sudo", "chown", "-R", "nobody:nogroup", cache_directory], check=True)
        subprocess.run(["sudo", "chmod", "750", cache_directory], check=True)
        return True
    except Exception as e:
        print(f"Failed to create cache directory or set permissions: {e}")
        return False   
  
def get_ssl_details(domain_name):
    alias = domain_name
    if domain_name.startswith("www."):
        
        domain_name = domain_name[4:]
    
        
    cert_path = f'/etc/letsencrypt/live/{domain_name}/fullchain.pem'  # Ensure the path is correct
    print(f"Checking certificate path: {cert_path}")  # Debugging line
    
    try:
        with open(cert_path, 'r') as f:
            fullchain_pem = f.read()
    except FileNotFoundError:
        return {
            "expiration_date": "Not Available",
            "certificate_type": "Unknown",
            "issuer": "Unknown",
            "certificate_validity": "Invalid or Not Found"
        }

    cert_info = parse_certificate(fullchain_pem)
    domains = cert_info.get("domains", [])

    # Check if alias matches any domain in certificate
    if alias not in domains:
        return {
            "expiration_date": "Not Available",
            "certificate_type": "Unknown",
            "issuer": "Unknown",
            "certificate_validity": "Invalid or Not Found"
        }

    
    
    try:
        # Get expiration date
        expiration_result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-enddate'],
            capture_output=True,
            text=True,
            check=True
        )
        expiration_output = expiration_result.stdout.strip()
        print(f"OpenSSL expiration output: {expiration_output}")  # Debugging line

        # Extract the expiration date
        expiration_date_str = expiration_output.split('=')[1]
        expiration_date = datetime.strptime(expiration_date_str, '%b %d %H:%M:%S %Y %Z')
        formatted_date = expiration_date.strftime('%d-%m-%y %I:%M %p')

        # Get certificate type
        key_type_result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-text'],
            capture_output=True,
            text=True,
            check=True
        )
        key_type_output = key_type_result.stdout.strip()
        print(f"OpenSSL key type output: {key_type_output}")  # Debugging line

        # Determine the certificate type
        if "RSA Public-Key" in key_type_output:
            cert_type = "RSA"
        elif "EC Public-Key" in key_type_output:
            cert_type = "ECC"
        else:
            cert_type = "Unknown"

        # Get certificate issuer and subject
        issuer_result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-issuer'],
            capture_output=True,
            text=True,
            check=True
        )
        issuer_output = issuer_result.stdout.strip()
        print(f"OpenSSL issuer output: {issuer_output}")  # Debugging line

        subject_result = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-subject'],
            capture_output=True,
            text=True,
            check=True
        )
        subject_output = subject_result.stdout.strip()
        print(f"OpenSSL subject output: {subject_output}")  # Debugging line

        # Extract the issuer and subject values
        issuer_name = issuer_output.split('=')[-1].split()[0]
        subject_name = subject_output.split('=')[-1]

        # Check if the certificate is self-signed
        if issuer_name.strip() == subject_name.strip():
            cert_validity = "Self-signed certificate"
        else:
            cert_validity = get_ssl_issuer_org(cert_path)

        return {
            "expiration_date": formatted_date,
            "certificate_type": cert_type,
            "issuer": issuer_name,
            "certificate_validity": cert_validity
        }
    except subprocess.CalledProcessError as e:
        print(f"Error running OpenSSL: {e.stderr.strip()}")  # Improved error logging
    except IndexError as e:
        print(f"Error parsing output: {e}")  # Log output for parsing errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # General error logging

    # Default values when an error occurs
    return {
        "expiration_date": "Not Available",
        "certificate_type": "Unknown",
        "issuer": "Unknown",
        "certificate_validity": "Invalid or Not Found"
    }
 
def get_ssl_issuer_org(cert_path: str) -> str:
    
    try:
        # Run OpenSSL command to get the issuer details
        result = subprocess.run(
            ["openssl", "x509", "-in", cert_path, "-noout", "-issuer"],
            check=True,
            capture_output=True,
            text=True
        )

        # Extract 'O=' (Organization) using regex
        
        match = re.search(r"O\s*=\s*([^,]+)", result.stdout)
        return match.group(1).strip() if match else "No Organization found"
    
    except subprocess.CalledProcessError as e:
        return f"Error reading certificate: {e.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"

      
def issue_ssl_certificate(domain: str, webroot_path: str) -> bool:
    if domain.startswith("www."):
        alias = domain
        domain = domain[4:]
        domains_list = [domain, alias]
    else:
        domains_list = [domain]        
     
    domain_args = []
    for d in domains_list:
        domain_args.extend(['-d', d])
        
    if getattr(settings, "MY_OS_NAME", "linux").strip().lower() in ("ubuntu", "debian", "linux mint"):
        reload_cmd = "systemctl restart apache2"
    else:
        reload_cmd = "systemctl restart httpd" 
    command = [
        '/root/.acme.sh/acme.sh',
        '--issue',
        *domain_args,
        '--cert-file', f'/etc/letsencrypt/live/{domain}/cert.pem',
        '--key-file', f'/etc/letsencrypt/live/{domain}/privkey.pem',
        '--fullchain-file', f'/etc/letsencrypt/live/{domain}/fullchain.pem',
        '-w', webroot_path,
        '--reloadcmd', reload_cmd,
        '--force',
        '--debug'
    ]

    try:
        # Execute the command
        create_letsencrypt_if_not_exist(domain);
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        email_ssl(domain)
        add_ssl_smtp_mail(domain)
        print(result.stdout.decode())
        logger.info(f"SSL issued successfully for {domain}:\n{result.stdout}")
        return True  # Return True if command executes successfully
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while issuing SSL for {domain}:\n{e.stderr}")
        print(f"An error occurred: {e.stderr.decode()}")
        return False  # Return False if command fails    


def get_dovecot_version():
    result = subprocess.run(["dovecot", "--version"], capture_output=True, text=True)
    return result.stdout.strip().split()[0].split("-")[0]

def is_dovecot_24_plus():
    version = get_dovecot_version()
    major, minor = map(int, version.split(".")[:2])
    return (major > 2) or (major == 2 and minor >= 4)

def email_ssl(domain):
    file_path = '/etc/dovecot/dovecot.conf'
    
    if is_dovecot_24_plus():
        block = f"""local_name {domain} {{
    ssl_server_cert_file = /etc/letsencrypt/live/{domain}/fullchain.pem
    ssl_server_key_file = /etc/letsencrypt/live/{domain}/privkey.pem
}}\n"""
    else:
        block = f"""local_name {domain} {{
    ssl_cert = </etc/letsencrypt/live/{domain}/fullchain.pem
    ssl_key = </etc/letsencrypt/live/{domain}/privkey.pem
}}\n"""

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        if f"local_name {domain} {{" in content:
            print(f"Block for '{domain}' already exists.")
            return

        with open(file_path, 'a') as f:
            f.write('\n' + block)

        print(f"Block for '{domain}' added.")
        subprocess.run(["sudo", "systemctl", "restart", "dovecot"], check=True)
    except Exception as e:
        print(f"Error updating file: {e}")


def add_ssl_smtp_mail(domain):
    key_path = f"/etc/letsencrypt/live/{domain}/privkey.pem"
    cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
    file_path="/etc/postfix/vmail_ssl.map"
    line_to_add = f"{domain} {key_path} {cert_path}\n"
    changed = False

    try:
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                if line_to_add in lines:
                    print("Line already exists. No change made.")
                else:
                    changed = True
        except FileNotFoundError:
            changed = True  # File doesn't exist, will create

        if changed:
            with open(file_path, "a") as f:
                f.write(line_to_add)
            print("Line added.")

        # Step 3: Run postmap -F
        subprocess.run(["postmap", "-F", f"hash:{file_path}"], check=True)
        print("postmap updated.")

        # Step 4: Restart Postfix
        subprocess.run(["systemctl", "restart", "postfix"], check=True)
        print("Postfix restarted.")

    except Exception as e:
        print(f"Error: {e}")        
 


def restart_pdns():
    try:
        # Execute the command to restart PowerDNS
        subprocess.check_call(['sudo', 'systemctl', 'restart', 'pdns'])
        print("PowerDNS service restarted successfully.")
        return True  # Indicate success
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart PowerDNS: {e}")
        return False  # Indicate failure   


def create_letsencrypt_if_not_exist(domain_name):
    folder_path = f"/etc/letsencrypt/live/{domain_name}"
    
    try:
        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")    


def vhost_action(domain_name, action):
    conf_file_path = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    # Check if the configuration file exists
    if not os.path.isfile(conf_file_path):
        print(
            f"Configuration file {conf_file_path} not found."
        )
        return False

    try:
        with open(conf_file_path, "r") as file:
            content = file.read()

        # ---------------------------------------------------------
        # Apache action paths
        # ---------------------------------------------------------

        action_paths = {
            "suspend": "/var/www/html/blocked",
            "bandwidth": "/var/www/html/bandwidth",
        }

        # ---------------------------------------------------------
        # Restore
        #
        # Look for a previously commented DocumentRoot:
        #
        # # DocumentRoot /home/babu/public_html
        # DocumentRoot /var/www/html/blocked
        # ---------------------------------------------------------

        if action == "restore":

            # Find the original commented DocumentRoot
            restore_match = re.search(
                r"^\s*#\s*DocumentRoot\s+(/home/\S+)"
                r"\s*$",
                content,
                re.MULTILINE
            )

            if not restore_match:
                print(
                    f"No original DocumentRoot found to restore "
                    f"in {conf_file_path}."
                )
                return False

            original_docroot = restore_match.group(1)

            # Find current DocumentRoot
            current_match = re.search(
                r"^\s*DocumentRoot\s+(\S+)\s*$",
                content,
                re.MULTILINE
            )

            if not current_match:
                print(
                    f"DocumentRoot not found in {conf_file_path}."
                )
                return False

            current_docroot = current_match.group(1)

            # Restore DocumentRoot
            content = re.sub(
                r"^(\s*)DocumentRoot\s+\S+\s*$",
                rf"\1DocumentRoot {original_docroot}",
                content,
                count=1,
                flags=re.MULTILINE
            )

            # Remove the backup comment
            content = re.sub(
                rf"^\s*#\s*DocumentRoot\s+"
                rf"{re.escape(original_docroot)}\s*$\n?",
                "",
                content,
                count=1,
                flags=re.MULTILINE
            )

            # Restore the first <Directory> path
            content = re.sub(
                r"^(\s*)<Directory\s+[^>]+>",
                rf"\1<Directory {original_docroot}>",
                content,
                count=1,
                flags=re.MULTILINE
            )

            with open(conf_file_path, "w") as file:
                file.write(content)

            print(
                f"DocumentRoot restored to {original_docroot} "
                f"in {conf_file_path}."
            )

            return True

        # ---------------------------------------------------------
        # Validate action
        # ---------------------------------------------------------

        if action not in action_paths:
            print(f"Invalid action: {action}")
            return False

        new_path = action_paths[action]

        # ---------------------------------------------------------
        # Find current DocumentRoot
        # ---------------------------------------------------------

        docroot_match = re.search(
            r"^\s*DocumentRoot\s+(\S+)\s*$",
            content,
            re.MULTILINE
        )

        if not docroot_match:
            print(
                f"DocumentRoot not found in {conf_file_path}."
            )
            return False

        current_path = docroot_match.group(1)

        # ---------------------------------------------------------
        # Check if action is already applied
        # ---------------------------------------------------------

        if current_path == new_path:
            print(
                f"Action '{action}' is already applied "
                f"to {current_path}. Skipping."
            )
            return False

        # ---------------------------------------------------------
        # Find original /home DocumentRoot
        # ---------------------------------------------------------

        if current_path.startswith("/home/"):

            old_home_path = current_path

            # Save original DocumentRoot as a comment
            backup_line = (
                f"# DocumentRoot {old_home_path}\n"
            )

            # Remove an old backup if one exists
            content = re.sub(
                r"^\s*#\s*DocumentRoot\s+/home/\S+\s*$\n?",
                "",
                content,
                flags=re.MULTILINE
            )

            # Put backup immediately before current DocumentRoot
            content = re.sub(
                r"^(\s*)DocumentRoot\s+\S+\s*$",
                rf"\1{backup_line}"
                rf"\1DocumentRoot {new_path}",
                content,
                count=1,
                flags=re.MULTILINE
            )

        else:
            # -----------------------------------------------------
            # Current DocumentRoot is already an action path.
            #
            # Just replace it.
            # -----------------------------------------------------

            content = re.sub(
                r"^(\s*)DocumentRoot\s+\S+\s*$",
                rf"\1DocumentRoot {new_path}",
                content,
                count=1,
                flags=re.MULTILINE
            )

        # ---------------------------------------------------------
        # Update the first <Directory> path
        # ---------------------------------------------------------

        content = re.sub(
            r"^(\s*)<Directory\s+[^>]+>",
            rf"\1<Directory {new_path}>",
            content,
            count=1,
            flags=re.MULTILINE
        )

        # ---------------------------------------------------------
        # Write configuration
        # ---------------------------------------------------------

        with open(conf_file_path, "w") as file:
            file.write(content)

        print(
            f"Action '{action}' successfully applied "
            f"to {conf_file_path}."
        )

        print(
            f"DocumentRoot: "
            f"{current_path} -> {new_path}"
        )

        return True

    except Exception as e:
        print(
            f"An error occurred: {e}"
        )
        return False

def normalize_domains(domain_name):
    """Validate and normalize the domain name by stripping unwanted prefixes."""
    
    # Remove 'http://' or 'https://'
    domain_name = re.sub(r'^https?://', '', domain_name)
    
    # Remove 'www.' prefix
    domain_name = re.sub(r'^www\.', '', domain_name)

    # Basic validation: Ensure the domain has at least one dot and only contains valid characters
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain_name):
        return None  # Invalid domain format

    return domain_name  # Return the normalized domain name   

def make_domain(domain_name, php_name, username_string, path):
    from users.database import get_user_data_by_id,add_domain_dns
    # Normalize and validate inputs
    domain_name = normalize_domains(domain_name.strip())
    if not domain_name:
        return {"success": False, "message": "Invalid domain format."}

    path = path.lstrip('/') or 'public_html'  # Default to 'public_html' if no path is provided
    doc_root = os.path.join("/home", username_string, path)

    try:
        # Check if domain already exists
        if Domain.objects.filter(domain=domain_name).exists():
            return {"success": False, "message": f"The domain '{domain_name}' already exists."}

        # Get user and package information
        user = User.objects.get(username=username_string)
        user_package = Package.objects.filter(id=get_user_data_by_id(user.id).get('pkg_id')).first()
        total_domains_count = Domain.objects.filter(userid=user.id).count()

        # Check if domain limit is exceeded
        if user_package.allowed_domains != 0 and total_domains_count >= user_package.allowed_domains:
            return {"success": False, "message": "Domain add limit exceeded."}

        # Manage listener and virtual host
        if not manage_listener_mapping("add", domain_name):
            return {"success": False, "message": f"Failed to add listener mapping for '{domain_name}'."}

        if not manage_virtual_host(domain_name, username_string):
            return {"success": False, "message": f"Failed to add virtual host for '{domain_name}'."}

        # SSL listener mapping and vhost file creation
        manage_ssl_listener_mapping("add", domain_name)
        create_vhost_file(domain_name, username_string, path)

        # Set folder permissions
        if not add_user_and_set_folder_permissions(username_string, f'/home/{username_string}', doc_root):
            return {"success": False, "message": f"Failed to set folder permissions for '{domain_name}'."}

        # Save domain to database
        domain_instance = Domain(
            domain=domain_name,
            userid=user,
            path=doc_root,
            line = 1,
            php=php_name
        )
        domain_instance.save()

        # Additional configurations
        new_php_version = php_name.replace('.', '')
        add_domain_dns(domain_instance.id, domain_name, user.id)
        change_php_version(domain_name, domain_name + '' + new_php_version, new_php_version)
        setup_dkim(domain_name)
        insert_dkim_record(domain_name,domain_instance.id,user.id)

        # Restart services
        restart_openlitespeed()
        restart_pdns()

        return {"success": True, "message": f"Domain '{domain_name}' added successfully!"}

    except User.DoesNotExist:
        return {"success": False, "message": f"User '{username_string}' does not exist."}
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

def read_php_ini(ini_file_path):
    # Example: Read the php.ini file and extract necessary settings
    settings = {}
    try:
        with open(ini_file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read full content
            for line in content.splitlines():  # Split by line for parsing
                line = line.strip()
                if line and not line.startswith(';'):  # Ignore comments and empty lines
                    if line.startswith('memory_limit'):
                        settings['memory_limit'] = line.split('=', 1)[1].strip()
                    elif line.startswith('upload_max_filesize'):
                        settings['upload_max_filesize'] = line.split('=', 1)[1].strip()
                    elif line.startswith('post_max_size'):
                        settings['post_max_size'] = line.split('=', 1)[1].strip()
                    elif line.startswith('max_execution_time'):
                        settings['max_execution_time'] = line.split('=', 1)[1].strip()
                    elif line.startswith('max_input_time'):
                        settings['max_input_time'] = line.split('=', 1)[1].strip()
                    elif line.startswith('allow_url_fopen'):
                        settings['allow_url_fopen'] = line.split('=', 1)[1].strip()
                    elif line.startswith('allow_url_include'):
                        settings['allow_url_include'] = line.split('=', 1)[1].strip()
                    elif line.startswith('display_errors'):
                        settings['display_errors'] = line.split('=', 1)[1].strip()
                    elif line.startswith('file_uploads'):
                        settings['file_uploads'] = line.split('=', 1)[1].strip()
            # Store full content for reference
            settings['content'] = content
    except Exception as e:
        print(f"Error reading php.ini: {e}")
    return settings


def fetch_php_settings_fun(php_version):
    current_settings = {}
    if php_version:
        if php_version.startswith('cgi'):
            new_php_version = php_version.replace('cgi ', '').replace('cgi', '').strip()
            ini_file_path = f'/etc/php/{new_php_version}/cgi/php.ini'
        else:
            new_php_version = str(php_version).replace('.', '')
            ini_file_path = f'/opt/olspanel/ol-php{new_php_version}/root/etc/php.ini'
            ini_file_path_old = f'/opt/olspanel/ol-php{new_php_version}/root/etc/php.ini'
        if os.path.exists(ini_file_path):
            current_settings = read_php_ini(ini_file_path)
        elif os.path.exists(ini_file_path_old):
            current_settings = read_php_ini(ini_file_path_old)
    return current_settings
    
    
def fetch_vhost_fun(domain):
    current_settings = {}
    vhost = f'{APACHE_CONFIG_DIR}/{domain}.conf'
    if os.path.exists(vhost):
        try:
            with open(vhost, 'r') as f: content = f.read()
            current_settings['status'] = 'success'
            current_settings['content'] = content
        except Exception as e:
            current_settings['status'] = 'error'
            current_settings['message'] = str(e)
    else:
        current_settings['status'] = 'error'
        current_settings['message'] = 'Apache vhost configuration not found'
    return current_settings
    

def reload_openlitespeed():
    os_name = getattr(settings, "MY_OS_NAME", "linux").strip().lower()
    service_name = "apache2" if os_name in ("ubuntu", "debian", "linux mint") else "httpd"
    apache_reloaded = False

    try:
        result = subprocess.run(
            ["sudo", "systemctl", "reload", service_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"Apache ({service_name}) reloaded successfully.")
            apache_reloaded = True
        else:
            print(f"Failed to reload Apache ({service_name}).")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)

    except Exception as e:
        print(f"Error reloading Apache: {e}")

    finally:
        try:
            restart_lsphp()
        except Exception as e:
            print(f"Error restarting PHP-FPM services: {e}")

    return apache_reloaded
    
def save_vhost_fun(domain, content):
    result = {}
    vhost = f'{APACHE_CONFIG_DIR}/{domain}.conf'
    if not os.path.exists(vhost): return {'status': 'error', 'message': 'Apache vhost configuration not found'}
    try:
        backup_path = vhost + ".bak"
        shutil.copy2(vhost, backup_path)
        with open(vhost, 'w') as f: f.write(content)
        result['status'] = 'success'
        result['message'] = 'Apache vhost configuration saved successfully'
        reload_openlitespeed()
    except Exception as e:
        result['status'] = 'error'
        result['message'] = str(e)
    return result

    
def get_ini_path_fun(php_version):
    new_php_version = str(php_version).replace('.', '')
    ini_file_path = f'/opt/olspanel/ol-php{new_php_version}/root/etc/php.ini'
    current_settings = ini_file_path if os.path.exists(ini_file_path) else None
    return current_settings

def get_php_version_hard():
    all_php_versions = ['7.3', '7.4', '8.0', '8.1', '8.2', '8.3','8.4','8.5']

    return all_php_versions  

def run_package_update_me():
    # Check for package manager existence
    if shutil.which('apt-get'):
        cmd = 'sudo apt-get update'
    elif shutil.which('dnf'):
        cmd = 'sudo dnf makecache'
    elif shutil.which('yum'):
        cmd = 'sudo yum makecache'
    elif shutil.which('zypper'):
        cmd = 'sudo zypper refresh'
    else:
        return {'status': 'error', 'message': 'No supported package manager found'}

    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return {'status': 'success', 'message': 'Package lists updated successfully'}
        else:
            return {'status': 'error', 'message': result.stderr.strip()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}  
    
    
def manage_php_extension(php_version, extension, action):
    try:
        os_name = getattr(settings, "MY_OS_NAME", "linux").lower()

        # Determine if CGI or lsphp version
        if php_version.startswith('cgi'):
            # Extract version number with dot, e.g. '7.4'
            try:
                version_num = php_version.split(' ')[1]
            except IndexError:
                return {'status': 'error', 'message': 'Invalid PHP version format.'}
            pkg_prefix = f'php{version_num}-'  # e.g. php7.4-mbstring
        else:
            # lsphp versions, remove dot for package names
            version_num = php_version.replace('.', '')
            pkg_prefix = f'ol-php{version_num}-'  # e.g. lsphp74-mbstring

        # Determine package manager & repo setup
        if os_name in ["ubuntu", "debian"]:
            # Add LiteSpeed repo only for lsphp packages (optional: skip for system php)
            if not php_version.startswith('cgi'):
                repo_cmd = "wget -O - https://olspanel.com/repo-files/repo.sh | sudo bash"
                subprocess.run(repo_cmd, shell=True, check=True)
                run_package_update_me()
            install_command = "apt-get"
        elif os_name in ["centos", "almalinux", "rocky", "rhel", "fedora", "oraclelinux", "amazonlinux"]:
            install_command = "dnf" if subprocess.run(["command", "-v", "dnf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0 else "yum"
        else:
            return {'status': 'error', 'message': f'Unsupported OS: {os_name}'}

        pkg_name = f"{pkg_prefix}{extension}"

        if action == "install":
            command = f"sudo {install_command} install {pkg_name} -y"
        elif action == "uninstall":
            command = f"sudo {install_command} remove {pkg_name} -y"
        else:
            return {'status': 'error', 'message': f'Unknown action: {action}'}

        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return {'status': 'success', 'message': f'Extension {extension} {action}ed successfully.'}
        else:
            return {'status': 'error', 'message': result.stderr.strip()}

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': f'Command failed: {e}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}





def fetch_php_extensions(php_version):
    all_extensions = ["curl", "mbstring", "xml", "json", "gd", "openssl", "mysql", "mysqli", "zip", "bcmath", "soap", "sockets", "intl", "exif", "opcache", "gettext", "imagick", "redis", "memcached", "fileinfo", "ftp", "zlib", "apcu", "imap", "ioncube", "ldap", "msgpack", "pgsql", "pspell", "snmp", "sqlite3", "sybase", "tidy", "pear"]

    if php_version.startswith("cgi"):
        lsphp = "php"
        try: version_num = php_version.split(" ")[1]
        except IndexError: version_num = ""
        new_php_version = version_num
        php_bin = f"/usr/bin/php-cgi{version_num}"
    else:
        lsphp = "ol-php"
        new_php_version = str(php_version).replace(".", "")
        php_bin = f"/opt/olspanel/ol-php{new_php_version}/root/bin/php"

    installed_exts = set()

    try:
        result = subprocess.run([php_bin, "-m"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            installed_exts = {x.strip().lower() for x in result.stdout.splitlines() if x.strip()}
    except Exception as e:
        print(f"Error checking PHP extensions: {e}")

    extension_aliases = {
        "mysql": {"mysqlnd", "mysqli", "pdo_mysql"},
        "opcache": {"zend opcache", "opcache"},
        "ioncube": {"ioncube loader", "the ioncube php loader", "ioncube"},
        "xml": {"xml", "simplexml", "xmlreader", "xmlwriter", "dom"},
        "zip": {"zip"},
        "json": {"json"},
        "fileinfo": {"fileinfo"},
        "pear": set(),
        "sybase": {"sybase", "pdo_dblib"},
    }

    available = []
    not_available = []

    for ext in all_extensions:
        aliases = extension_aliases.get(ext, {ext})

        if aliases and aliases.intersection(installed_exts):
            available.append(ext)
        elif ext == "pear":
            pear_path = f"/opt/olspanel/ol-php{new_php_version}/root/bin/pear"
            if os.path.isfile(pear_path):
                available.append(ext)
            else:
                not_available.append(ext)
        else:
            not_available.append(ext)

    return {"available": sorted(set(available)), "not_available": sorted(set(not_available))}

def install_php(versions):
    version = versions.replace('.', '')
    os_name = getattr(settings, "MY_OS_NAME", "linux")
    os_f = getattr(settings, 'MY_OS_VERSION', 'linux')

    if os_name == "ubuntu" or os_name == "debian":
        install_command = "apt-get"
    elif os_name in ["centos", "almalinux", "rocky", "rhel", "fedora", "oraclelinux", "amazonlinux"]:
        # Use `dnf` if available, otherwise fallback to `yum`
        install_command = "dnf" if subprocess.run(["command", "-v", "dnf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0 else "yum"
    else:
        return {'status': 'error', 'message': f'Unsupported OS: {os_name}'}

    try:
        # Step 1: Add necessary repositories based on the OS
        if os_name == "ubuntu":
            subprocess.run("sudo apt-get install -y software-properties-common", shell=True, check=True)
            subprocess.run("sudo add-apt-repository ppa:openlitespeed/php", shell=True, check=True)
            subprocess.run("sudo apt-get update", shell=True, check=True)
        elif os_name == "debian" :
            subprocess.run("sudo apt-get update", shell=True, check=True)
            
        elif os_name in ["centos", "almalinux", "rocky", "rhel", "fedora", "oraclelinux", "amazonlinux"]:
            # Additional repository setup for CentOS/AlmaLinux/RHEL
            subprocess.run(f"sudo {install_command} install -y epel-release", shell=True, check=True)
            subprocess.run(f"sudo {install_command} install -y ol-php{version} ol-php{version}-common ol-php{version}-mysqlnd", shell=True, check=True)

        # Step 2: Install PHP and dependencies based on the OS
        if os_name == "ubuntu":
            subprocess.run(f"sudo {install_command} install -y ol-php{version} lsphp{version}-common ol-php{version}-mysqlnd", shell=True, check=True)
        elif os_name in ["centos", "almalinux", "rocky", "rhel", "fedora", "oraclelinux", "amazonlinux"]:
            subprocess.run(f"sudo {install_command} install -y ol-php{version} lsphp{version}-common ol-php{version}-mysqlnd", shell=True, check=True)

        # Return success message
        return {'status': 'success', 'message': f'PHP {version} installed successfully.'}

    except subprocess.CalledProcessError as e:
        return {'status': 'error', 'message': f'Unsupported php version {versions} for OS {os_name} {os_f}'}
            
            
            
       
def write_httpd_config():
    try:
        # Apache ModSecurity configuration
        if os.path.isdir("/etc/httpd/modsecurity.d"):
            config_file = f"{APACHE_CONFIG_DIR}/mod_security.conf"
            custom_rules_dir = "/etc/httpd/modsecurity.d/local_rules"
            apache_service = "httpd"
            apachectl = shutil.which("apachectl") or "/usr/sbin/apachectl"

        elif os.path.isdir("/etc/modsecurity"):
            config_file = "/etc/modsecurity/modsecurity.conf"
            custom_rules_dir = "/etc/modsecurity/local_rules"
            apache_service = "apache2"
            apachectl = shutil.which("apache2ctl") or "/usr/sbin/apache2ctl"

        else:
            return {
                "status": "error",
                "message": "Apache ModSecurity directory not found."
            }

        os.makedirs(custom_rules_dir, exist_ok=True)

        # Copy application custom rules
        result = copy_mod_file()
        if isinstance(result, dict) and result.get("status") == "error":
            return result

        result = copy_mod_file_rule()
        if isinstance(result, dict) and result.get("status") == "error":
            return result

        # Prepare CRS exclusion files
        result = rename_exclusion_rules_file()
        if isinstance(result, dict) and result.get("status") == "error":
            return result

        # Read existing ModSecurity configuration
        if os.path.isfile(config_file):
            with open(
                config_file,
                "r",
                encoding="utf-8"
            ) as file:
                content = file.read()
        else:
            content = ""

        # Ensure custom local rules are loaded
        local_rules_include = (
            f"IncludeOptional {custom_rules_dir}/*.conf"
        )

        if local_rules_include not in content:
            if content and not content.endswith("\n"):
                content += "\n"

            content += (
                "\n# OLSPanel custom ModSecurity rules\n"
                f"{local_rules_include}\n"
            )

        # Create/update Apache configuration
        with open(
            config_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)

        # Debian/Ubuntu
        if apache_service == "apache2":
            if shutil.which("a2enmod"):
                subprocess.run(
                    ["a2enmod", "security2"],
                    check=True
                )

        # Validate Apache
        result = subprocess.run(
            [apachectl, "-t"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": (
                    "Apache configuration test failed: "
                    + (result.stderr or result.stdout)
                )
            }

        return {
            "status": "success",
            "message": (
                f"Apache ModSecurity configuration updated: "
                f"{config_file}"
            )
        }

    except Exception as ex:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(ex)}"
        }

def install_modsecurity_and_crs():
    try:
        # Step 1: Detect package manager
        if shutil.which("dnf"):
            package_manager = "dnf"
        elif shutil.which("yum"):
            package_manager = "yum"
        elif shutil.which("apt-get"):
            package_manager = "apt"
        elif shutil.which("zypper"):
            package_manager = "zypper"
        else:
            return {
                "status": "error",
                "message": (
                    "Unsupported package manager. "
                    "Supported: yum, dnf, apt, zypper."
                )
            }

        # Step 2: Install Apache ModSecurity + OWASP CRS
        if package_manager in ["yum", "dnf"]:

            subprocess.run(
                [
                    package_manager,
                    "install",
                    "mod_security",
                    "mod_security_crs",
                    "-y"
                ],
                check=True
            )

        elif package_manager == "apt":

            subprocess.run(
                ["apt-get", "update"],
                check=True
            )

            subprocess.run(
                [
                    "apt-get",
                    "install",
                    "libapache2-mod-security2",
                    "modsecurity-crs",
                    "-y"
                ],
                check=True
            )

            if shutil.which("a2enmod"):
                subprocess.run(
                    ["a2enmod", "security2"],
                    check=True
                )

        elif package_manager == "zypper":
            return {
                "status": "error",
                "message": (
                    "Apache ModSecurity package names for zypper "
                    "must be configured for the target distribution."
                )
            }

        # ---------------------------------------------------------
        # Step 3: Detect Apache ModSecurity directory
        # ---------------------------------------------------------

        if os.path.isdir("/etc/httpd/modsecurity.d"):
            modsecurity_dir = "/etc/httpd/modsecurity.d"
            modsecurity_conf = f"{APACHE_CONFIG_DIR}/mod_security.conf"
            apachectl = (
                shutil.which("apachectl")
                or "/usr/sbin/apachectl"
            )
            apache_service = "httpd"

        elif os.path.isdir("/etc/modsecurity"):
            modsecurity_dir = "/etc/modsecurity"
            modsecurity_conf = "/etc/modsecurity/modsecurity.conf"
            apachectl = (
                shutil.which("apache2ctl")
                or "/usr/sbin/apache2ctl"
            )
            apache_service = "apache2"

        else:
            return {
                "status": "error",
                "message": (
                    "ModSecurity was installed but the Apache "
                    "ModSecurity directory was not found."
                )
            }

        # ---------------------------------------------------------
        # Step 4: Ensure ModSecurity configuration exists
        # ---------------------------------------------------------

        if not os.path.isfile(modsecurity_conf):

            recommended = (
                "/etc/modsecurity/modsecurity.conf-recommended"
            )

            if os.path.isfile(recommended):
                shutil.copy2(
                    recommended,
                    modsecurity_conf
                )
            else:
                return {
                    "status": "error",
                    "message": (
                        "ModSecurity configuration file not found: "
                        + modsecurity_conf
                    )
                }

        # ---------------------------------------------------------
        # Step 5: Set DetectionOnly initially
        # ---------------------------------------------------------

        with open(
            modsecurity_conf,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()

        engine_pattern = r"(?m)^(\s*SecRuleEngine\s+)\w+"

        if re.search(engine_pattern, content):

            content = re.sub(
                engine_pattern,
                r"\1DetectionOnly",
                content,
                count=1
            )

        else:
            content += "\nSecRuleEngine DetectionOnly\n"

        with open(
            modsecurity_conf,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)

        # ---------------------------------------------------------
        # Step 6: Check OWASP CRS
        # ---------------------------------------------------------

        crs_files = [
            "/etc/httpd/modsecurity.d/crs-setup.conf",
            "/etc/httpd/modsecurity.d/activated_rules",
            "/usr/share/modsecurity-crs/owasp-crs.load",
            "/etc/modsecurity/crs/crs-setup.conf",
        ]

        crs_found = any(
            os.path.exists(path)
            for path in crs_files
        )

        if not crs_found:
            return {
                "status": "error",
                "message": (
                    "OWASP CRS was not found after installation."
                )
            }

        # ---------------------------------------------------------
        # Step 7: Write Apache configuration
        # ---------------------------------------------------------

        config_result = write_httpd_config()

        if config_result.get("status") != "success":
            return config_result

        # ---------------------------------------------------------
        # Step 8: Final Apache configuration test
        # ---------------------------------------------------------

        result = subprocess.run(
            [apachectl, "-t"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "message": (
                    "Apache configuration test failed: "
                    + (result.stderr or result.stdout)
                )
            }

        # ---------------------------------------------------------
        # Step 9: Reload Apache
        # ---------------------------------------------------------
        replace_config_value_mod('SecRuleEngine', 'On')
        replace_config_value_mod('SecAuditEngine', 'on')
        reload_openlitespeed()

        return {
            "status": "success",
            "message": (
                "Apache ModSecurity and OWASP CRS have been "
                "installed and configured successfully."
            )
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Error during installation: {str(e)}"
        }

    except Exception as ex:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(ex)}"
        }


def copy_mod_file():
    try:
        # Get Django root path
        django_root = settings.BASE_DIR

        source_file = os.path.join(
            django_root,
            "media",
            "csf",
            "owasp-master.conf"
        )

        # Apache destination
        if os.path.isdir("/etc/httpd/modsecurity.d"):
            destination_dir = (
                "/etc/httpd/modsecurity.d/local_rules"
            )
        elif os.path.isdir("/etc/modsecurity"):
            destination_dir = (
                "/etc/modsecurity/local_rules"
            )
        else:
            return {
                "status": "error",
                "message": (
                    "Apache ModSecurity directory not found."
                )
            }

        os.makedirs(
            destination_dir,
            exist_ok=True
        )

        destination_file = os.path.join(
            destination_dir,
            "owasp-master.conf"
        )

        if os.path.exists(source_file):

            shutil.copy2(
                source_file,
                destination_file
            )

            return {
                "status": "success",
                "message": (
                    f"File copied successfully to "
                    f"{destination_file}"
                )
            }

        return {
            "status": "error",
            "message": (
                f"Source file does not exist: "
                f"{source_file}"
            )
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error copying file: {e}"
        }


def copy_mod_file_rule():
    try:
        # Get Django root path
        django_root = settings.BASE_DIR

        source_file = os.path.join(
            django_root,
            "media",
            "csf",
            "arule.conf"
        )

        # Apache destination
        if os.path.isdir("/etc/httpd/modsecurity.d"):
            destination_dir = (
                "/etc/httpd/modsecurity.d/local_rules"
            )
        elif os.path.isdir("/etc/modsecurity"):
            destination_dir = (
                "/etc/modsecurity/local_rules"
            )
        else:
            return {
                "status": "error",
                "message": (
                    "Apache ModSecurity directory not found."
                )
            }

        os.makedirs(
            destination_dir,
            exist_ok=True
        )

        destination_file = os.path.join(
            destination_dir,
            "arule.conf"
        )

        if os.path.exists(source_file):

            shutil.copy2(
                source_file,
                destination_file
            )

            return {
                "status": "success",
                "message": (
                    f"File copied successfully to "
                    f"{destination_file}"
                )
            }

        return {
            "status": "error",
            "message": (
                f"Source file does not exist: "
                f"{source_file}"
            )
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error copying file: {e}"
        }


def rename_exclusion_rules_file():
    try:
        # Find CRS rules directory
        possible_rules_dirs = [
            "/etc/httpd/modsecurity.d/activated_rules",
            "/etc/httpd/modsecurity.d/rules",
            "/usr/share/modsecurity-crs/rules",
            "/etc/modsecurity/crs/rules",
        ]

        rules_dir = None

        for directory in possible_rules_dirs:
            if os.path.isdir(directory):
                rules_dir = directory
                break

        if not rules_dir:
            return {
                "status": "success",
                "message": (
                    "CRS rules directory not found. "
                    "No exclusion files changed."
                )
            }

        # BEFORE CRS
        original_file = os.path.join(
            rules_dir,
            "REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example"
        )

        renamed_file = os.path.join(
            rules_dir,
            "REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf"
        )

        # AFTER CRS
        original_file2 = os.path.join(
            rules_dir,
            "RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example"
        )

        renamed_file2 = os.path.join(
            rules_dir,
            "RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf"
        )

        changed = []

        if (
            os.path.exists(original_file)
            and not os.path.exists(renamed_file)
        ):
            shutil.copy2(
                original_file,
                renamed_file
            )

            changed.append(renamed_file)

        if (
            os.path.exists(original_file2)
            and not os.path.exists(renamed_file2)
        ):
            shutil.copy2(
                original_file2,
                renamed_file2
            )

            changed.append(renamed_file2)

        return {
            "status": "success",
            "message": "CRS exclusion rules prepared.",
            "files": changed
        }

    except Exception as e:
        return {
            "status": "error",
            "message": (
                f"An error occurred: {str(e)}"
            )
        }        
        
        
        
def check_modsecurity_rule():
    config_file = f"{APACHE_CONFIG_DIR}/zz-modsecurity-custom.conf"
    rule_line = "IncludeOptional /etc/httpd/modsecurity.d/local_rules/*.conf"

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            for line in file:
                stripped_line = line.strip()

                # Check if the line matches and is not commented out
                if (
                    stripped_line == rule_line
                    and not stripped_line.startswith("#")
                ):
                    return True

        return False

    except FileNotFoundError:
        print(f"Configuration file not found: {config_file}")
        return False

    except Exception as ex:
        print(f"Error checking ModSecurity configuration: {ex}")
        return False


def toggle_comment(comment=False):
    config_file = "/usr/local/lsws/conf/httpd_config.conf"
    rule_line = "modsecurity_rules_file /usr/local/lsws/conf/owasp/coreruleset/owasp-master.conf"
    try:
        # Read the file content
        with open(config_file, 'r') as file:
            lines = file.readlines()

        # Process the lines
        updated_lines = []
        line_found = False

        for line in lines:
            stripped_line = line.lstrip()  # Remove leading spaces for comparison
            if rule_line in stripped_line:  # Match both commented and uncommented versions
                line_found = True
                if comment and not stripped_line.startswith("#"):  # Add #
                    updated_lines.append("#" + line)  # Add a comment if not already commented
                elif not comment and stripped_line.startswith("#"):  # Remove #
                    updated_lines.append(line.lstrip()[1:])  # Uncomment by removing the first #
                else:
                    updated_lines.append(line)  # Keep the line as is
            else:
                updated_lines.append(line)  # Keep other lines unchanged

        if not line_found:
            print(f"Line not found: {rule_line}")
            return False

        # Write back the updated content
        with open(config_file, 'w') as file:
            file.writelines(updated_lines)

        return True
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


           
def _apache_modsecurity_config():
    return f'{APACHE_CONFIG_DIR}/mod_security.conf'


def _apache_modsecurity_key(name):
    mapping = {
        'modsecurity': 'SecRuleEngine',
    }

    return mapping.get(name, name)


def get_config_value_mod(name):
    filename = _apache_modsecurity_config()

    # Old key -> Apache key
    if name == 'modsecurity':
        apache_name = 'SecRuleEngine'
    else:
        apache_name = name

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Match directive + value
                match = re.match(
                    rf'^{re.escape(apache_name)}\s+(.+?)\s*$',
                    line,
                    re.IGNORECASE
                )

                if match:
                    value = match.group(1).strip()

                    # Old UI expects modsecurity as on/off
                    if name == 'modsecurity':
                        return 'on' if value.lower() == 'on' else 'off'

                    return value

        print(
            f"Config '{apache_name}' not found in {filename}."
        )
        return None

    except Exception as e:
        print(f"Error retrieving value: {e}")
        return None


def replace_config_value_mod(name, new_value):
    filename = _apache_modsecurity_config()

    # Old OpenLiteSpeed key -> Apache key
    if name == 'modsecurity':
        apache_name = 'SecRuleEngine'
    else:
        apache_name = name

    try:
        with open(filename, 'r+', encoding='utf-8') as f:
            content = f.read()

            pattern = rf'^(\s*){re.escape(apache_name)}\s+.*$'

            if re.search(
                pattern,
                content,
                re.MULTILINE | re.IGNORECASE
            ):
                new_line = rf'\1{apache_name} {new_value}'

                content = re.sub(
                    pattern,
                    new_line,
                    content,
                    flags=re.MULTILINE | re.IGNORECASE
                )

                f.seek(0)
                f.write(content)
                f.truncate()

                print(
                    f"Replaced '{name}' -> '{apache_name}' "
                    f"with '{new_value}' in {filename}."
                )

                return True

            print(
                f"Config '{apache_name}' not found in {filename}."
            )
            return False

    except Exception as e:
        print(f"Error replacing value: {e}")
        return False
        
def restart_lsphp():
    try:
        result = subprocess.run(["systemctl", "list-units", "--type=service", "--all", "--no-legend", "--no-pager"], capture_output=True, text=True, check=True)
        services = re.findall(r'\b(ol-php\d+-fpm)\.service\b', result.stdout)
        if not services:
            print("No OLSPanel PHP-FPM services found."); return False
        for service in sorted(set(services)):
            subprocess.run(["sudo", "systemctl", "reload", service], check=True)
            print(f"{service} reloaded successfully.")
        print("All OLSPanel PHP-FPM services reloaded successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading PHP-FPM: {e}"); return False
    except Exception as e:
        print(f"Error restarting PHP-FPM: {e}"); return False

def copy_mod_file():
    # Get the Django root path
    django_root = settings.BASE_DIR

    # Construct the correct source and destination file paths
    source_file = os.path.join(django_root, 'media', 'csf', 'owasp-master.conf')
    destination_file = '/usr/local/lsws/conf/owasp/coreruleset/owasp-master.conf'

    # Check if the source file exists before proceeding
    if os.path.exists(source_file):
        try:
            # Run the copy operation using shutil.copy
            shutil.copy(source_file, destination_file)
            return "File copied successfully!"  # Return a success message
        except Exception as e:
            return f"Error copying file: {e}"  # Return the error message if an exception occurs
    else:
        return f"Source file does not exist: {source_file}"  # Return a message if the source file doesn't exist        


def copy_mod_file_rule():
    # Get the Django root path
    django_root = settings.BASE_DIR

    # Construct the correct source and destination file paths
    source_file = os.path.join(django_root, 'media', 'csf', 'arule.conf')
    destination_file = '/usr/local/lsws/conf/owasp/coreruleset/arule.conf'

    # Check if the source file exists before proceeding
    if os.path.exists(source_file):
        try:
            # Run the copy operation using shutil.copy
            shutil.copy(source_file, destination_file)
            return "File copied successfully!"  # Return a success message
        except Exception as e:
            return f"Error copying file: {e}"  # Return the error message if an exception occurs
    else:
        return f"Source file does not exist: {source_file}"  # Return a message if the source file doesn't exist 


def read_php_conf(path):
    settings = {'log_errors': 'Off', 'error_log': 'Off', 'error_reporting': '0', 'display_errors': 'Off'}
    try:
        with open(path, 'r') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith(('php_admin_value', 'php_admin_flag', 'php_value', 'php_flag')):
                    parts = stripped.split(None, 2)
                    if len(parts) == 3:
                        directive, key, value = parts
                        settings[key] = value.strip('"').strip()
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return settings


def get_current_php_version(domain_name):
    vhost_file_path = f"{APACHE_CONFIG_DIR}/{domain_name}.conf"

    try:
        if not os.path.isfile(vhost_file_path):
            print(f"Configuration file {vhost_file_path} does not exist.")
            return None

        with open(vhost_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        match = re.search(
            r"/run/olspanel/ol-php(\d+)/[^/\s|]+\.sock",
            content
        )

        if not match:
            print(f"PHP-FPM socket not found in {vhost_file_path}")
            return None

        version_number = match.group(1)

        # 83 -> 8.3
        if len(version_number) >= 2:
            php_version = f"{version_number[:-1]}.{version_number[-1]}"
        else:
            php_version = version_number

        return php_version

    except Exception as e:
        print(f"Error reading PHP version: {e}")
        return None

def write_php_conf(path, new_settings: dict):
    domain_name = None

    if path:
        domain_name = os.path.basename(path)
        domain_name = re.sub(r'\.conf$', '', domain_name, flags=re.IGNORECASE)

    try:
        current_php_version = get_current_php_version(domain_name)

        if not current_php_version:
            print(f"Could not determine current PHP version for {domain_name}")
            return False

        php_version_number = current_php_version.replace('.', '')
        php_root = f'/opt/olspanel/ol-php{php_version_number}/root'
        path = f'{php_root}/etc/php-fpm.d/{domain_name}.conf'

        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                for k, v in new_settings.items():
                    if k == 'open_basedir':
                        continue
                    f.write(f'php_admin_value[{k}] = {v}\n')
            return True

        existing_settings = {}

        for i, line in enumerate(lines):
            stripped = line.strip()

            match = re.match(
                r'^(php_admin_value|php_admin_flag)\[([^\]]+)\]\s*=\s*(.*)$',
                stripped
            )

            if match:
                existing_settings[match.group(2)] = (
                    match.group(1),
                    match.group(3),
                    i
                )

        for key, value in new_settings.items():
            key = str(key).strip()

            if key == 'open_basedir':
                continue

            value = str(value).strip()

            directive = (
                existing_settings[key][0]
                if key in existing_settings
                else (
                    'php_admin_flag'
                    if value.lower() in ('on', 'off')
                    else 'php_admin_value'
                )
            )

            if key in existing_settings:
                lines[existing_settings[key][2]] = (
                    f'{directive}[{key}] = {value}\n'
                )
            else:
                lines.append(
                    f'{directive}[{key}] = {value}\n'
                )

        with open(path, 'w') as f:
            f.writelines(lines)

        return True

    except Exception as e:
        print(f"Error writing {path}: {e}")
        return False
        
def check_mod_installed():
    mod_conf = f"{APACHE_CONFIG_DIR}/mod_security.conf"
    return os.path.exists(mod_conf)    
    
    
  
    
def get_vhost_directory(domain):
    vhost_directory = f"{APACHE_CONFIG_DIR}/{domain}"

    return vhost_directory 
    
def get_vhost_file(domain):
    vhost_directory = f"{APACHE_CONFIG_DIR}/{domain}.conf"

    return vhost_directory   


def enable_cgroups():
    import time
    with open(LISTENER_CONFIG_FILE, "r") as f:
        content = f.read()

    pattern = r"CGIRLimit\s*\{.*?\}"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print("CGIRLimit block not found")
        return False

    block = match.group(0)

    if re.search(r"cgroups\s+\d+", block):
        new_block = re.sub(
            r"cgroups\s+\d+",
            "cgroups                 2",
            block
        )
    else:
        new_block = block[:-1] + "\n  cgroups                 2\n}"

    if block == new_block:
        print("cgroups already set correctly")
        return False

    content = content.replace(block, new_block)

    with open(LISTENER_CONFIG_FILE, "w") as f:
        f.write(content)

    print("Updated cgroups to 2")

    restart_lsphp()

    print("LSWS restarted")
    return True        
    

def get_error_reporting_value(value):
    value = str(value).strip().strip('"').strip("'")
    value = re.sub(r'\s+', ' ', value)

    error_options = {
        'Off': '0',
        'No Errors': '0',

        'E_ALL & ~E_NOTICE': '32759',
        'All Except Notices': '32759',

        'E_ALL': '32767',
        'All Errors': '32767',

        'E_ERROR': '1',
        'Fatal Errors': '1',

        'E_WARNING': '2',
        'Warnings': '2',

        'E_PARSE': '4',
        'Parse Errors': '4',

        'E_NOTICE': '8',
        'Notices': '8',

        'E_DEPRECATED': '8192',
        'Deprecated Notices': '8192',
    }

    if value.isdigit():
        return value

    return error_options.get(value, '0')

  


def get_php_settings(php_version: str, override_path: str = None):
    domain_name = None

    if override_path:
        domain_name = os.path.basename(override_path)
        domain_name = re.sub(r'\.conf$', '', domain_name, flags=re.IGNORECASE)
    settings = {
        'memory_limit': None,
        'upload_max_filesize': None,
        'post_max_size': None,
        'max_execution_time': None,
        'max_input_time': None,
        'allow_url_fopen': None,
        'allow_url_include': None,
        'display_errors': None,
        'file_uploads': None,
        'log_errors': 'Off',
        'error_log': 'Off',
        'error_reporting': '0'
    }

    boolean_keys = {
        'allow_url_fopen',
        'allow_url_include',
        'display_errors',
        'file_uploads',
        'log_errors'
    }

    if not php_version:
        return settings

    new_php_version = re.sub(r'\D', '', str(php_version))

    if not new_php_version:
        return settings

    php_root = f'/opt/olspanel/ol-php{new_php_version}/root'
    ini_file_path = f'{php_root}/etc/php.ini'

    # Helper function to normalize boolean strings (on, off, 1, 0, yes, no, true, false)
    def normalize_bool(val: str) -> str:
        return 'On' if val.lower() in ('on', '1', 'yes', 'true') else 'Off'

    # ---------------------------------------------------------
    # 1. Read global php.ini
    # ---------------------------------------------------------
    try:
        if os.path.isfile(ini_file_path):
            with open(ini_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith(';') or '=' not in line:
                        continue

                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key not in settings:
                        continue

                    if key == 'error_reporting':
                        settings[key] = get_error_reporting_value(value)
                    elif key in boolean_keys:
                        settings[key] = normalize_bool(value)
                    else:
                        settings[key] = value

    except Exception as e:
        print(f"Error reading {ini_file_path}: {e}")

    # ---------------------------------------------------------
    # 2. Read PHP-FPM domain configuration (Overrides php.ini)
    # ---------------------------------------------------------
    if domain_name:
        fpm_conf_path = f'{php_root}/etc/php-fpm.d/{domain_name}.conf'

        try:
            if not os.path.isfile(fpm_conf_path):
                print(f"FPM configuration not found: {fpm_conf_path}")
                return settings

            with open(fpm_conf_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith(';'):
                        continue

                    # Single Regex Match for php_admin_flag, php_flag, php_admin_value, php_value
                    match = re.match(
                        r'(?:php_admin_flag|php_flag|php_admin_value|php_value)\s*\[\s*([^\]]+)\s*\]\s*=\s*(.*)',
                        line,
                        re.IGNORECASE
                    )

                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip().strip('"').strip("'")

                        if key not in settings:
                            continue

                        # Apply override logic
                        if key == 'error_reporting':
                            settings[key] = get_error_reporting_value(value)
                        elif key in boolean_keys:
                            settings[key] = normalize_bool(value)
                        else:
                            settings[key] = value

                        print(f"FPM OVERRIDE APPLIED: {key} = {settings[key]}")

        except Exception as e:
            print(f"Error reading {fpm_conf_path}: {e}")

    return settings
    
    
    

def create_ols_node_context(version, target_path, startup_file, domain, old_context=None):
    
    from users.models import Domain

    try:
        # Normalize URL contexts.
        old_path = str(old_context or '').strip('/')
        context_path = str(target_path or '').strip('/')

        domain_s = Domain.objects.filter(domain=domain).first()
        if not domain_s:
            return {
                'status': 'error',
                'message': f'Domain not found: {domain}'
            }

        username = str(domain_s.userid)
        doc_root = os.path.realpath(domain_s.path)

        if not os.path.isdir(doc_root):
            return {
                'status': 'error',
                'message': f'Document root not found: {doc_root}'
            }

        # Always resolve target_path relative to the domain document root.
        # "/" or "" means doc_root; "node" means doc_root/node.
        app_directory = os.path.realpath(
            os.path.join(doc_root, context_path)
        )

        try:
            if os.path.commonpath([doc_root, app_directory]) != doc_root:
                return {
                    'status': 'error',
                    'message': 'Invalid application directory'
                }
        except ValueError:
            return {
                'status': 'error',
                'message': 'Invalid application directory'
            }

        if not os.path.isdir(app_directory):
            return {
                'status': 'error',
                'message': f'Application directory not found: {app_directory}'
            }

        # Validate Node.js binary.
        binpath = f'/usr/local/olspanel/bin/nodejs/{version}/bin/node'

        if not os.path.isfile(binpath) or not os.access(binpath, os.X_OK):
            return {
                'status': 'error',
                'message': f'Node.js binary not found or not executable: {binpath}'
            }

        # Resolve startup file relative to the application directory.
        startup_file = str(startup_file or '').strip()

        if not startup_file:
            return {
                'status': 'error',
                'message': 'Startup file is required'
            }

        if os.path.isabs(startup_file):
            app_file = os.path.realpath(startup_file)
        else:
            app_file = os.path.realpath(
                os.path.join(app_directory, startup_file)
            )

        try:
            if os.path.commonpath([app_directory, app_file]) != app_directory:
                return {
                    'status': 'error',
                    'message': 'Invalid startup file path'
                }
        except ValueError:
            return {
                'status': 'error',
                'message': 'Invalid startup file path'
            }

        if not os.path.isfile(app_file):
            return {
                'status': 'error',
                'message': f'Node.js startup file not found: {app_file}'
            }

        ensure_node_launcher()

        conf_dir = '/usr/local/olspanel/node/conf'
        os.makedirs(conf_dir, mode=0o755, exist_ok=True)

        app_id = re.sub(
            r'[^a-zA-Z0-9]+',
            '-',
            f'{domain}-{context_path or "root"}'
        ).strip('-').lower()

        conf_file = os.path.join(conf_dir, f'{app_id}.conf')
        conf_exists = os.path.isfile(conf_file)

        # Reuse the existing application's port when possible.
        port = None

        if conf_exists:
            with open(conf_file, 'r') as f:
                for line in f:
                    match = re.match(r'^\s*port\s*=\s*(\d+)\s*$', line)
                    if match:
                        port = int(match.group(1))
                        break

        if port is None:
            result = generate_app_port(username, 'node')

            if result and result.get('status') == 'success':
                port = result.get('port')

            if port is None:
                return {
                    'status': 'error',
                    'message': f'Unable to allocate an application port: {result}'
                }

        conf_content = f"""runtime_user={username}
runtime_group={username}
port={port}
host=127.0.0.1
node_binary={binpath}
app_script={app_file}
"""

        with open(conf_file, 'w') as f:
            f.write(conf_content)

        os.chmod(conf_file, 0o640)

        restart_node_launcher()

        # Configure Apache using "/" for the domain root.
        proxy_result = create_apache_node_proxy(
            domain,
            port,
            '/' + context_path if context_path else '/'
        )

        if not proxy_result or proxy_result.get('status') != 'updated':
            return {
                'status': 'error',
                'message': (
                    'Node.js configuration was saved, but Apache proxy '
                    'configuration failed: '
                    + (
                        proxy_result.get('message', 'Unknown error')
                        if proxy_result else 'No result returned'
                    )
                ),
                'config': conf_file,
                'port': port
            }

        # Delete the old context only after the new proxy is configured.
        if old_context is not None and old_path != context_path:
            delete_ols_node_context(domain, old_path)

        return {
            'status': 'updated' if conf_exists else 'created',
            'message': (
                f'Node.js configuration '
                f'{"updated" if conf_exists else "created"}: {conf_file}'
            ),
            'config': conf_file,
            'port': port,
            'context_path': '/' + context_path if context_path else '/',
            'app_directory': app_directory,
            'startup_file': app_file,
            'node_binary': binpath
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }



def create_apache_node_proxy(domain, port, context_path='/node'):
    try:
       

        conf_file = f"{APACHE_CONFIG_DIR}/{domain}.conf"
        proxy_start = "# OLSPanel Node.js Proxy Start"
        proxy_end = "# OLSPanel Node.js Proxy End"

        
        context_path = "/" + context_path.strip("/") if context_path.strip("/") else "/"

        if context_path == "/":
            proxy_content = f"""{proxy_start}
    ProxyRequests Off
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:{port}/
    ProxyPassReverse / http://127.0.0.1:{port}/
    {proxy_end}"""
        else:
            proxy_content = f"""{proxy_start}
    ProxyRequests Off
    ProxyPreserveHost On
    ProxyPass {context_path}/ http://127.0.0.1:{port}/
    ProxyPassReverse {context_path}/ http://127.0.0.1:{port}/
    ProxyPass {context_path} http://127.0.0.1:{port}/
    ProxyPassReverse {context_path} http://127.0.0.1:{port}/
    {proxy_end}"""


        if not os.path.isfile(conf_file):
            return {
                'status': 'not_found',
                'message': f"Apache vhost configuration not found: {conf_file}"
            }

        with open(conf_file, 'r') as f:
            content = f.read()

        # Find every VirtualHost block, including HTTP and HTTPS.
        pattern = re.compile(
            r'<VirtualHost\b[^>]*>.*?</VirtualHost>',
            re.IGNORECASE | re.DOTALL
        )

        matches = list(pattern.finditer(content))

        if not matches:
            return {
                'status': 'error',
                'message': f"No VirtualHost blocks found in {conf_file}"
            }

        updated_content = content
        updated_count = 0

        # Process blocks in reverse order to preserve offsets.
        for match in reversed(matches):
            block = match.group(0)

            if proxy_start in block and proxy_end in block:
                start = block.index(proxy_start)
                end = block.index(proxy_end, start) + len(proxy_end)
                block = block[:start] + proxy_content + block[end:]
            else:
                closing_tag = re.search(
                    r'</VirtualHost\s*>',
                    block,
                    re.IGNORECASE
                )

                if not closing_tag:
                    continue

                block = (
                    block[:closing_tag.start()]
                    + '\n\n    ' + proxy_content + '\n\n'
                    + block[closing_tag.start():]
                )

            updated_content = (
                updated_content[:match.start()]
                + block
                + updated_content[match.end():]
            )
            updated_count += 1

        if updated_count == 0:
            return {
                'status': 'error',
                'message': f"Unable to update VirtualHost blocks in {conf_file}"
            }

        with open(conf_file, 'w') as f:
            f.write(updated_content)

        # Validate the Apache configuration before reloading.
        result = subprocess.run(
            ['httpd', '-t'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f"Apache configuration test failed: {result.stderr or result.stdout}"
            }

        reload_openlitespeed()

        return {
            'status': 'updated',
            'message': f"Node.js proxy configured for {domain}{context_path} in {updated_count} VirtualHost block(s)",
            'config': conf_file,
            'port': port
        }

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def ensure_node_launcher():
    try:
        launcher_path = "/usr/local/bin/node-launcher"

        if os.path.isfile(launcher_path) and os.access(launcher_path, os.X_OK):
            return {
                'status': 'exists',
                'message': 'Node launcher is already installed.'
            }

        result = subprocess.run(
            "curl -fsSL https://olspanel.com/extra/node_setup.sh | sed 's/\\r$//' | bash",
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            return {
                'status': 'error',
                'message': result.stderr or result.stdout or 'Node launcher setup failed.'
            }

        if not os.path.isfile(launcher_path) or not os.access(launcher_path, os.X_OK):
            return {
                'status': 'error',
                'message': 'Setup finished, but /usr/local/bin/node-launcher is missing or not executable.'
            }

        return {
            'status': 'installed',
            'message': 'Node launcher installed successfully.'
        }

    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'message': 'Node launcher setup timed out.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }




def generate_app_port(username, app_type, max_attempts=100):
    
    try:
        user_info = pwd.getpwnam(username)
        uid_digit = user_info.pw_uid % 10

        app_types = {
            'node': 1,
            'python': 2,
            'php': 3,
            'other': 4,
        }

        app_type = app_type.lower()

        if app_type not in app_types:
            return {
                'status': 'error',
                'message': f'Unsupported application type: {app_type}'
            }

        type_digit = app_types[app_type]

        for _ in range(max_attempts):
            random_digits = random.randint(0, 999)
            port = int(f"{uid_digit}{type_digit}{random_digits:03d}")

            # Skip privileged ports.
            if port < 1024:
                continue

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(('127.0.0.1', port))
                    return {
                        'status': 'success',
                        'port': port,
                        'username': username,
                        'uid_digit': uid_digit,
                        'app_type': app_type,
                    }
                except OSError:
                    continue

        return {
            'status': 'error',
            'message': 'Unable to find an available port after maximum attempts.'
        }

    except KeyError:
        return {
            'status': 'error',
            'message': f'Linux user not found: {username}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }




def delete_ols_node_context(domain, context_path):
    """
    Remove the Node.js configuration file and Apache proxy blocks
    for the specified domain and context.
    """
    try:
       

        context_path = '' if not context_path or context_path.strip() == '/' else context_path.strip('/')

        app_id = re.sub(
            r'[^a-zA-Z0-9]+',
            '-',
            f"{domain}-{context_path or 'root'}"
        ).strip('-').lower()

        # Remove the C++ Node.js manager configuration.
        conf_dir = "/usr/local/olspanel/node/conf"
        node_conf_file = os.path.join(conf_dir, f"{app_id}.conf")

        if os.path.isfile(node_conf_file):
            os.remove(node_conf_file)

        # Remove the Apache proxy block from every VirtualHost.
        apache_file = f"{APACHE_CONFIG_DIR}/{domain}.conf"
        proxy_start = "# OLSPanel Node.js Proxy Start"
        proxy_end = "# OLSPanel Node.js Proxy End"

        if os.path.isfile(apache_file):
            with open(apache_file, 'r') as f:
                content = f.read()

            pattern = re.compile(
                re.escape(proxy_start) + r'.*?' + re.escape(proxy_end),
                re.DOTALL
            )

            # Remove only blocks matching this application's context.
            def remove_matching_block(match):
                block = match.group(0)

                path_match = re.search(
                    r'^\s*ProxyPass\s+(\S+)\s+http://127\.0\.0\.1:\d+/',
                    block,
                    re.MULTILINE
                )

                if not path_match:
                    return block

                configured_path = path_match.group(1).rstrip('/') or '/'
                requested_path = '/' + context_path if context_path else '/node'

                if configured_path == requested_path:
                    return ''

                return block

            updated_content = pattern.sub(remove_matching_block, content)

            if updated_content != content:
                with open(apache_file, 'w') as f:
                    f.write(updated_content)

                result = subprocess.run(
                    ['httpd', '-t'],
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    return {
                        'status': 'error',
                        'message': f"Apache configuration test failed: {result.stderr or result.stdout}. Restore the previous Apache configuration before retrying."
                    }

                reload_openlitespeed()
        restart_node_launcher()
        return {
            'status': 'deleted',
            'message': f"Node.js configuration and Apache proxy removed for {domain}/{context_path or '/'}",
            'config': node_conf_file
        }

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
      
        
        

def create_app_js(target_folder, file_name):
    """
    Create a folder if it doesn't exist and generate app.js with default content.
    """
    try:
        if not os.path.exists(target_folder):
            os.makedirs(target_folder, exist_ok=True)

        app_js_path = os.path.join(target_folder, file_name)

        if not os.path.exists(app_js_path):
            content = """var http = require('http');

// Safety Check: Exit if C++ launcher didn't pass the variables
if (!process.env.PORT) {
    console.error("Fatal Error: No PORT environment variable was provided.");
    process.exit(1);
}

var server = http.createServer(function(req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    var message = 'It works!\\n',
        version = 'NodeJS ' + process.versions.node + '\\n',
        response = [message, version].join('\\n');
    res.end(response);
});

var port = parseInt(process.env.PORT, 10);
var host = process.env.HOST || '127.0.0.1';

server.listen(port, host, function() {
    console.log('-> Node.js process successfully started on ' + host + ':' + port);
});
"""
            with open(app_js_path, 'w') as f:
                f.write(content)

            return {
                'status': 'success',
                'message': f"Created {file_name} in {target_folder}"
            }
        else:
            return {
                'status': 'exists',
                'message': f"{file_name} already exists"
            }

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def restart_node_launcher():
    try:
        result = subprocess.run(
            ['systemctl', 'restart', 'olnode'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return {
                'status': 'success',
                'message': 'Node launcher service restarted successfully.'
            }

        return {
            'status': 'error',
            'message': result.stderr.strip() or result.stdout.strip() or 'Failed to restart olnode service.'
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
        
        
        
def restart_node(path):
    try:
        restart_node_launcher()

       

    except Exception as e:
        return {'status': 'error', 'message': str(e)}        
        
        
def get_server_conf_path():    
    CONF_FILE_PATH = '/usr/local/lsws/conf/httpd_config.conf'
    return CONF_FILE_PATH    
        
def read_litespeed_conf(file_path):
    config = {}
    if not os.path.exists(file_path):
        return config

    with open(file_path, 'r') as f:
        content = f.read()

    # Simple Apache directives
    for key in [
        'ServerRoot', 'Listen', 'User', 'Group', 'ServerAdmin',
        'ServerName', 'DocumentRoot', 'DirectoryIndex',
        'ErrorLog', 'LogLevel', 'CustomLog', 'EnableSendfile',
        'EnableMMAP', 'KeepAlive', 'MaxKeepAliveRequests',
        'KeepAliveTimeout', 'LimitRequestFieldSize',
        'LimitRequestFields', 'LimitRequestBody', 'Timeout',
        'HostnameLookups', 'ServerTokens', 'ServerSignature',
        'AddDefaultCharset', 'TypesConfig', 'MIMEMagicFile',
        'CacheRoot', 'CacheDirLevels', 'CacheDirLength',
        'CacheMaxExpire', 'CacheEnable', 'CacheDisable',
        'AllowOverride', 'Options', 'Require'
    ]:
        matches = re.findall(
            rf'^[ \t]*{re.escape(key)}[ \t]+([^#\r\n]*?)\s*$',
            content,
            re.MULTILINE | re.IGNORECASE
        )
        config[key] = matches[-1].strip() if matches else ''

    # Apache cache enable/disable status
    cache_enable = re.search(
        r'^[ \t]*CacheEnable[ \t]+disk[ \t]+/',
        content, re.MULTILINE | re.IGNORECASE
    )
    cache_disable = re.search(
        r'^[ \t]*CacheDisable[ \t]+/',
        content, re.MULTILINE | re.IGNORECASE
    )
    config['apacheCacheEnabled'] = (
        'On' if cache_enable and not cache_disable else 'Off'
    )

    # Read important configuration sections as complete text
    for key, pattern in {
        'Directory': r'<Directory\b[^>]*>.*?</Directory>',
        'FilesMatch': r'<FilesMatch\b[^>]*>.*?</FilesMatch>',
        'IfModule': r'<IfModule\b[^>]*>.*?</IfModule>',
    }.items():
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        config[key] = matches

    return config




def write_litespeed_conf(file_path, new_settings):
    if not os.path.exists(file_path):
        print(f"Apache configuration file not found: {file_path}")
        return False

    config_keys = {
        'ServerRoot', 'Listen', 'User', 'Group', 'ServerAdmin',
        'ServerName', 'DocumentRoot', 'ErrorLog', 'LogLevel',
        'EnableSendfile', 'EnableMMAP', 'KeepAlive',
        'MaxKeepAliveRequests', 'KeepAliveTimeout',
        'LimitRequestFieldSize', 'LimitRequestFields',
        'LimitRequestBody', 'Timeout', 'HostnameLookups',
        'ServerTokens', 'ServerSignature', 'AddDefaultCharset',
        'TypesConfig', 'MIMEMagicFile', 'CacheRoot',
        'CacheDirLevels', 'CacheDirLength', 'CacheMaxExpire'
    }

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        settings = {
            key: str(value).strip()
            for key, value in new_settings.items()
            if key in config_keys
            and value is not None
            and str(value).strip()
        }

        updated_lines = []
        seen_keys = set()

        for line in lines:
            stripped = line.strip()

            if not stripped or stripped.startswith('#'):
                updated_lines.append(line)
                continue

            if 'apacheCacheEnabled' in new_settings and re.match(
                r'^\s*Cache(?:Enable\s+disk|Disable)\s+/',
                line,
                re.IGNORECASE
            ):
                continue

            matched = False

            for key, value in settings.items():
                if re.match(
                    rf'^\s*{re.escape(key)}(?:\s|$)',
                    line,
                    re.IGNORECASE
                ):
                    updated_lines.append(f'{key} {value}\n')
                    seen_keys.add(key)
                    matched = True
                    break

            if not matched:
                updated_lines.append(line)

        missing = [
            (key, value)
            for key, value in settings.items()
            if key not in seen_keys
        ]

        if missing:
            insert_at = len(updated_lines)

            for i, line in enumerate(updated_lines):
                if re.match(
                    r'^\s*IncludeOptional\s+conf\.d/\*\.conf',
                    line,
                    re.IGNORECASE
                ):
                    insert_at = i
                    break

            if insert_at > 0 and not updated_lines[insert_at - 1].endswith('\n'):
                updated_lines[insert_at - 1] += '\n'

            new_lines = ['\n']
            new_lines.extend(
                f'{key} {value}\n' for key, value in missing
            )
            new_lines.append('\n')

            updated_lines[insert_at:insert_at] = new_lines

        # Apply the global Apache disk-cache toggle.
        
        # Apply the Apache disk-cache toggle inside mod_cache_disk.c.
        if 'apacheCacheEnabled' in new_settings:
            enabled = str(
                new_settings['apacheCacheEnabled']
            ).strip().lower() in ('on', 'true', '1', 'yes')

            directive = (
                '        CacheEnable disk /\n'
                if enabled
                else '        CacheDisable /\n'
            )

            # Remove existing active cache toggle directives.
            updated_lines = [
                line for line in updated_lines
                if line.strip().startswith('#')
                or not re.match(
                    r'^\s*Cache(?:Enable\s+disk|Disable)\s+/',
                    line,
                    re.IGNORECASE
                )
            ]

            # Update CacheRoot for Apache's cache directory.
            for i, line in enumerate(updated_lines):
                if re.match(
                    r'^\s*CacheRoot(?:\s|$)',
                    line,
                    re.IGNORECASE
                ):
                    updated_lines[i] = (
                        '        CacheRoot "/var/cache/apache2/default"\n'
                    )

            # Find the inner mod_cache_disk.c block and insert
            # the toggle before its closing </IfModule>.
            disk_start = None
            disk_end = None
            depth = 0

            for i, line in enumerate(updated_lines):
                stripped = line.strip()

                if stripped.startswith('#'):
                    continue

                if disk_start is None and re.match(
                    r'^<IfModule\s+mod_cache_disk\.c\s*>$',
                    stripped,
                    re.IGNORECASE
                ):
                    disk_start = i
                    depth = 1
                    continue

                if disk_start is not None:
                    if re.match(r'^<IfModule\b', stripped, re.IGNORECASE):
                        depth += 1
                    elif re.match(
                        r'^</IfModule\s*>$',
                        stripped,
                        re.IGNORECASE
                    ):
                        depth -= 1
                        if depth == 0:
                            disk_end = i
                            break

            if disk_start is not None and disk_end is not None:
                updated_lines.insert(
                    disk_end,
                    '\n' + directive
                )
            else:
                # Create the complete cache block if it doesn't exist.
                cache_block = [
                    '\n<IfModule mod_cache.c>\n',
                    '    <IfModule mod_cache_disk.c>\n',
                    '        CacheRoot "/var/cache/apache2/default"\n',
                    '        CacheDirLevels 2\n',
                    '        CacheDirLength 1\n',
                    '        CacheMaxExpire 86400\n',
                    '\n',
                    directive,
                    '\n',
                    '    </IfModule>\n',
                    '</IfModule>\n',
                ]
                updated_lines.extend(cache_block)

        if updated_lines and not updated_lines[-1].endswith('\n'):
            updated_lines[-1] += '\n'

        with open(file_path, 'w') as f:
            f.writelines(updated_lines)

        print(f"Apache configuration written: {file_path}")
        return True

    except Exception as e:
        print(f"Failed to write Apache configuration: {e}")
        return False           
                
                
def handle_php_tune(request):
    from django.shortcuts import render
    from users.models import Domain

    domains = Domain.objects.all()

    if request.method == 'POST':
        php_domain = request.POST.get('php_domain')

        if not php_domain:
            messages.warning(request, "Please select a domain.")
            return render(request, 'whm/fpm_tune.html', {
                'php_domain': domains
            })

        
        
        version_number=get_current_php_version(php_domain)
        php_version_number = version_number.replace('.', '')
        php_dir = f"/opt/olspanel/ol-php{php_version_number}/root"
        fpm_dir = f"{php_dir}/etc/php-fpm.d"
        conf_file = f"{fpm_dir}/{php_domain}.conf"
        
        

        pool_settings = {
            'pm.max_requests': request.POST.get('max_requests', '20').strip(),
            'pm.max_children': request.POST.get('max_children', '5').strip(),
            'pm.process_idle_timeout': request.POST.get(
                'process_idle_timeout', '10s'
            ).strip(),
        }

        ini_settings = {
            'allow_url_fopen': 'On' if request.POST.get('allow_url_fopen') else 'Off',
            'log_errors': 'On' if request.POST.get('log_errors') else 'Off',
            'short_open_tag': 'On' if request.POST.get('short_open_tag') else 'Off',
            'error_log': request.POST.get('error_log', '').strip(),
            'disable_functions': request.POST.get('disable_functions', '').strip(),
            'error_reporting': request.POST.get('error_reporting', '0').strip(),
        }

        try:
            write_php_fpm_settings(
                conf_file,
                pool_settings,
                ini_settings
            )

            restart_lsphp()
            messages.success(request, "PHP-FPM configuration updated successfully.")

        except Exception as e:
            messages.warning(request, f"Failed to update config: {str(e)}")

    return render(request, 'whm/fpm_tune.html', {
        'php_domain': domains
    })
    
    
def get_php_tune_settings(domain_name):
    current_settings = {}

    if domain_name:
        version_number=get_current_php_version(domain_name)
        php_version_number = version_number.replace('.', '')
        php_dir = f"/opt/olspanel/ol-php{php_version_number}/root"
        fpm_dir = f"{php_dir}/etc/php-fpm.d"
        conf_file = f"{fpm_dir}/{domain_name}.conf"
       

        if os.path.exists(conf_file):
            current_settings = read_php_fpm_settings(conf_file)

    return current_settings    


def read_php_fpm_settings(conf_file):
    settings = {
        'pool': {
            'pm': '',
            'pm.max_children': '',
            'pm.max_requests': '',
            'pm.process_idle_timeout': '',
        },
        'ini': {},
        'ini_locks': {},
    }

    if not os.path.isfile(conf_file):
        return settings

    with open(conf_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith(('#', ';')):
            continue

        pool_match = re.match(
            r'^(pm|pm\.max_requests|pm\.max_children|'
            r'pm\.process_idle_timeout)\s*=\s*(.*?)\s*$',
            line
        )

        if pool_match:
            settings['pool'][pool_match.group(1)] = pool_match.group(2)
            continue

        ini_match = re.match(
            r'^(php_admin_value|php_admin_flag|'
            r'php_value|php_flag)\[([^\]]+)\]\s*=\s*(.*?)\s*$',
            line
        )

        if ini_match:
            directive, key, value = ini_match.groups()

            settings['ini'][key] = value
            settings['ini_locks'][key] = directive.startswith('php_admin_')

    return settings



def write_php_fpm_settings(conf_file, pool_settings, ini_settings):
    if not os.path.isfile(conf_file):
        raise FileNotFoundError(f"PHP-FPM config not found: {conf_file}")

    with open(conf_file, 'r') as f:
        lines = f.readlines()

    pool_keys = {
        'pm.max_requests',
        'pm.max_children',
        'pm.process_idle_timeout',
    }

    ini_keys = {
        key: value
        for key, value in ini_settings.items()
        if key in {
            'allow_url_fopen',
            'log_errors',
            'short_open_tag',
            'error_log',
            'disable_functions',
            'error_reporting',
        }
    }

    updated_pool = set()
    updated_ini = set()
    new_lines = []

    pool_pattern = re.compile(
        r'^(pm\.max_requests|pm\.max_children|'
        r'pm\.process_idle_timeout)\s*='
    )

    ini_pattern = re.compile(
        r'^(php_admin_value|php_admin_flag|'
        r'php_value|php_flag)\[([^\]]+)\]\s*='
    )

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith(('#', ';')):
            new_lines.append(line)
            continue

        pool_match = pool_pattern.match(stripped)

        if pool_match:
            key = pool_match.group(1)

            if key in pool_settings:
                if key not in updated_pool:
                    new_lines.append(
                        f"{key} = {pool_settings[key]}\n"
                    )
                    updated_pool.add(key)
                continue

        ini_match = ini_pattern.match(stripped)

        if ini_match:
            directive, key = ini_match.groups()

            if key in ini_keys:
                if key not in updated_ini:
                    value = str(ini_keys[key])

                    if directive.endswith('_flag'):
                        value = 'On' if value.lower() in (
                            '1', 'on', 'true', 'yes'
                        ) else 'Off'

                    new_lines.append(
                        f"{directive}[{key}] = {value}\n"
                    )
                    updated_ini.add(key)
                continue

        new_lines.append(line)

    for key in pool_keys:
        if key in pool_settings and key not in updated_pool:
            new_lines.append(f"{key} = {pool_settings[key]}\n")

    for key, value in ini_keys.items():
        if key in updated_ini:
            continue

        directive = (
            'php_admin_flag'
            if key in ('allow_url_fopen', 'log_errors', 'short_open_tag')
            else 'php_admin_value'
        )

        if directive.endswith('_flag'):
            value = 'On' if str(value).lower() in (
                '1', 'on', 'true', 'yes'
            ) else 'Off'

        new_lines.append(f"{directive}[{key}] = {value}\n")

    temp_file = conf_file + '.tmp'

    with open(temp_file, 'w') as f:
        f.writelines(new_lines)

    os.chmod(temp_file, os.stat(conf_file).st_mode)
    os.replace(temp_file, conf_file)


def handle_litespeed_conf(request):
    from django.shortcuts import render, redirect
    
    current_settings = read_litespeed_conf(APACHE_CONFIG_FILE)

    if request.method == 'POST':
        new_settings = {
            'ServerRoot': request.POST.get('ServerRoot', '').strip(),
            'Listen': request.POST.get('Listen', '').strip(),
            'User': request.POST.get('User', '').strip(),
            'Group': request.POST.get('Group', '').strip(),
            'ServerAdmin': request.POST.get('ServerAdmin', '').strip(),
            'ServerName': request.POST.get('ServerName', '').strip(),
            'DocumentRoot': request.POST.get('DocumentRoot', '').strip(),
            'DirectoryIndex': request.POST.get('DirectoryIndex', '').strip(),
            'KeepAlive': request.POST.get('KeepAlive', 'Off'),
            'MaxKeepAliveRequests': request.POST.get('MaxKeepAliveRequests', '').strip(),
            'KeepAliveTimeout': request.POST.get('KeepAliveTimeout', '').strip(),
            'Timeout': request.POST.get('Timeout', '').strip(),
            'LimitRequestFieldSize': request.POST.get('LimitRequestFieldSize', '').strip(),
            'LimitRequestFields': request.POST.get('LimitRequestFields', '').strip(),
            'LimitRequestBody': request.POST.get('LimitRequestBody', '').strip(),
            'EnableSendfile': request.POST.get('EnableSendfile', 'off'),
            'EnableMMAP': request.POST.get('EnableMMAP', 'off'),
            'ErrorLog': request.POST.get('ErrorLog', '').strip(),
            'LogLevel': request.POST.get('LogLevel', 'warn'),
            'HostnameLookups': request.POST.get('HostnameLookups', 'Off'),
            'ServerTokens': request.POST.get('ServerTokens', 'Prod'),
            'ServerSignature': request.POST.get('ServerSignature', 'Off'),
            'CacheRoot': request.POST.get('CacheRoot', '').strip(),
            'CacheDirLevels': request.POST.get('CacheDirLevels', '').strip(),
            'CacheDirLength': request.POST.get('CacheDirLength', '').strip(),
            'CacheMaxExpire': request.POST.get('CacheMaxExpire', '').strip(),
            'apacheCacheEnabled': 'On' if request.POST.get('apacheCacheEnabled') else 'Off',
            'browserCacheEnabled': 'On' if request.POST.get('browserCacheEnabled') else 'Off',
            'gzipEnabled': 'On' if request.POST.get('gzipEnabled') else 'Off',
        }

        try:
            if not write_litespeed_conf(APACHE_CONFIG_FILE, new_settings):
                messages.warning(request, "Failed to update Apache configuration.")
                return redirect('/whm/litespeed_conf/')

            test_result = subprocess.run(
                ['sudo', 'httpd', '-t'],
                capture_output=True,
                text=True
            )

            if test_result.returncode != 0:
                messages.warning(
                    request,
                    f"Apache configuration test failed: {test_result.stderr or test_result.stdout}"
                )
                return redirect('/whm/litespeed_conf/')

            reload_openlitespeed()

            messages.success(request, "Apache configuration updated successfully.")

        except Exception as e:
            messages.warning(request, f"Failed to update Apache configuration: {str(e)}")

        return redirect('/whm/litespeed_conf/')

    return render(request, 'whm/apache_conf.html', {
        'current_settings': current_settings,
        'log_levels': [
            'emerg', 'alert', 'crit', 'error', 'warn',
            'notice', 'info', 'debug', 'trace1'
        ],
        'server_tokens': ['Full', 'OS', 'Minimal', 'Minor', 'Major', 'Prod'],
    })
    
    
    
def get_openlitespeed_version():
    try:
        result = subprocess.run(
            ["apachectl", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            # Extract the version number using a regular expression
            match = re.search(r"Apache/(\d+\.\d+\.\d+)", result.stdout)
            if match:
                return match.group(1)
            else:
                return "Version not found"
        else:
            return "Unknown"
    except Exception as e:
        return f"Error: {e}"      