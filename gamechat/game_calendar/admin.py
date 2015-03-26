from django.contrib import admin

# Register your models here.
from game_calendar.models import Article, Event


admin.site.register(Article)
admin.site.register(Event)
