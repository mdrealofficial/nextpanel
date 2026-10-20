import os
from django.conf import settings


def get_server_type():
    source_file = os.path.join(settings.BASE_DIR, 'etc', 'server_type')

    if not os.path.exists(source_file):
        return 'openlitespeed'

    try:
        with open(source_file, 'r') as file:
            server_type = file.read().strip().lower()

        if server_type in ('apache', 'openlitespeed', 'ols', 'apache_openlitespeed','nginx', 'apache_nginx'):
            return server_type

        return 'openlitespeed'

    except (OSError, IOError):
        return 'openlitespeed'




def get_service_names():
    os_name = getattr(settings, "MY_OS_NAME", "linux")
    server_type = get_server_type().strip().lower()

    if os_name in ("ubuntu", "debian"):
        ftpserver = "pure-ftpd-mysql"
        apache = "apache2"
    else:
        ftpserver = "pure-ftpd"
        apache = "httpd"

    if os_name == "debian":
        openlitespeed = "lsws"
    else:
        openlitespeed = "openlitespeed"

    services_to_check = {
        "mariadb": "MariaDB",
    }

    if server_type in ("apache", "apache_openlitespeed", "apache_nginx"):
        services_to_check[apache] = "Apache"

    if server_type in ("openlitespeed", "ols", "apache_openlitespeed"):
        services_to_check[openlitespeed] = "OpenLiteSpeed"

    if server_type in ("nginx", "apache_nginx"):
        services_to_check["nginx"] = "Nginx"

    services_to_check.update({
        "pdns": "DNS",
        "dovecot": "IMAP",
        "postfix": "Mail server",
        ftpserver: "FTP Server",
        "opendkim": "OpenDkim",
    })

    return services_to_check



SERVER_TYPE = get_server_type()

if SERVER_TYPE == 'apache':
    from .server_core_apache import *
else:
    from .server_core_openlitespeed import *
