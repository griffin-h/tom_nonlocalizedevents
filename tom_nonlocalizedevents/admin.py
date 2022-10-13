from django.contrib import admin

from .models import EventCandidate, EventLocalization, NonLocalizedEvent

# Register your models here.
admin.site.register(EventCandidate)
admin.site.register(EventLocalization)
admin.site.register(NonLocalizedEvent)
