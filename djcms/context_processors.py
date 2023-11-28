from django.conf import settings # import the settings file

def admin_media(request):
    return settings.GLOBAL_SETTINGS
