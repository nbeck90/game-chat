from django.forms import ModelForm
from game_calendar.models import Event
from profiles.models import Profile


class EventForm(ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'time', 'invitees', 'description']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        profile = Profile.objects.get(user=self.initial['user'])
        self.fields['invitees'].queryset = profile.get_friends()
