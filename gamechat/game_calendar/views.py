from game_calendar.models import Event
from django.shortcuts import render
from django.views.generic.edit import CreateView


class EventCreate(CreateView):
    model = Event


def return_event(request):
    from datetime import datetime
    from django.http import HttpResponse
    import json

    json_list = []
    for event in Event.objects.all():
        json_entry = {
            'title': event.title,
            'start': event.date.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': False
            }
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')


def calendar(request):
    return render(request, 'game_calendar/calendar.html')
