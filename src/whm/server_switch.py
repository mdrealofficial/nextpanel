import os


def convert_conf(SERVER_TYPE):
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

    for domain_instance in domains:
        domain_name = normalize_domains(domain_instance.domain.strip())
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
            replace_docroot_in_virtual_conf(vhost_file, path)

        change_php_version(
            domain_name,
            domain_name + new_php_version,
            new_php_version,
        )

    return {
        "success": True,
        "total": domains.count(),
        "message": "All domain configurations processed successfully.",
    }
    
    
    
def app_convert(SERVER_TYPE):
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

    for app in apps:
        domain = Domain.objects.filter(id=app.domain_id).first()

        if not domain:
            continue

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
                

    

    return {
        "success": True,
        "total": apps.count(),
        "message": "All app configurations processed successfully.",
    }