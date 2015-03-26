from django.contrib import admin

# Register your models here.
from game_calendar.models import Event

admin.site.register(Event)
