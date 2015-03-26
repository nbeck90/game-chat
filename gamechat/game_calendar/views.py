from game_calendar.models import Event
from game_calendar.forms import EventForm
from profiles.models import Profile
from django.shortcuts import render
from django.views.generic.edit import CreateView


class EventCreate(CreateView):
    model = Event
    form_class = EventForm 

    def get_initial(self):
        initial = super(EventCreate, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.creator = Profile.objects.get(
            pk=self.request.user.id)
        return super(EventCreate, self).form_valid(form)


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
