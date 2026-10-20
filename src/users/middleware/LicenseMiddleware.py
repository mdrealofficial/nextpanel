"""
NextPanel Open Access Middleware.
Unlocks all features, routes, APIs, branding, and quotas with unlimited lifetime status.
"""

class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Inject lifetime community/enterprise license meta attributes
        request.META['LICENSE_KEY'] = 'NEXTPANEL-COMMUNITY-UNLIMITED'
        request.META['LICENSE_EXPIRE'] = '2099-12-31T23:59:59Z'
        request.META['LICENSE_TYPE'] = 'basic,pro,enterprise'
        request.META['LICENSE_STATUS'] = 'active'

        # Allow all requests through without blocking
        return self.get_response(request)