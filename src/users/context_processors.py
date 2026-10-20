import requests
from .plugin import * 
from users.models import AppSettings
from users.function import * 

def dynamic_plugins(request):
    """Make plugin lists available globally (e.g., sidebar)"""
    # Optional parameter example (softaculous)
    softaculous = True

    return {
        'software_plugin': get_software_plugins_list(softaculous),
        'domain_plugin': get_domain_plugins_list(),
        'file_plugin': get_file_plugins_list(),
        'security_plugin': get_security_plugins_list(),
        'database_plugin': get_database_plugins_list(),
        'email_plugin': get_email_plugins_list(),
        'advance_plugin': get_advance_plugins_list(),
    }

def branding(request):

    # NextPanel default branding
    branding_data = {
        "brand_title": "NextPanel",
        "brand_image": "/media/logo.png",
        "brand_icon": "/media/logo.png",
        "brand_color": "#2563eb",
    }

    keys = branding_data.keys()
    try:
        qs = AppSettings.objects.filter(setting_key__in=keys)
        for item in qs:
            value = item.setting_value
            if value and str(value).strip():
                branding_data[item.setting_key] = value
    except Exception:
        pass

    return {"branding": branding_data}