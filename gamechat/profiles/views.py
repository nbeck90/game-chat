from django.shortcuts import render
from models import Profile
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from forms import ProfileForm


def profile(request, slug):
    context = {}
    try:
        profile = Profile.objects.get(slug=slug)
        context['profile'] = profile
        context['friends'] = profile.get_friends()
    except Profile.DoesNotExist:
        pass

    return render(request, 'profiles/profile.html', context)


class ProfileEdit(UpdateView):
    model = Profile
    template_name = 'profile_edit.html'
    form_class = ProfileForm

    fields = (
        'friends',
        'blocking')
    success_url = reverse_lazy('profile')
