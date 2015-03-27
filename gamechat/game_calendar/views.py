from game_calendar.models import Event
from game_calendar.forms import EventForm
from profiles.models import Profile
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.db.models import Q


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


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'game_calendar/event_detail.html', {'event': event})


class EventDelete(DeleteView):
    model = Event


def return_event(request):
    from datetime import datetime
    from django.http import HttpResponse
    import json

    profile = request.user.profile
    json_list = []
    for event in Event.objects.filter(Q(attending=profile) |
                                      Q(creator=profile)):
        attending_list = []
        for attendee in event.attending.all():
            attending_list.append(attendee.user.username)
        print event.creator
        json_entry = {
            'title': event.title,
            'start': event.time.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': False,
            'pk': str(event.pk)
            }
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')


def calendar(request):
    return render(request, 'game_calendar/calendar.html')
