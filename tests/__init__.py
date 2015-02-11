from django.conf import settings
import django

settings.configure()

try:
    django.setup()
except AttributeError:  # django 1.4
    pass
