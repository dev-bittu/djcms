from django.conf import settings # import the settings file

def admin_media(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_URL": settings.SITE_URL
    }
