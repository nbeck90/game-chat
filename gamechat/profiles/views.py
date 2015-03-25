from django.shortcuts import render
from models import Profile
from django.shortcuts import redirect
from django.views.generic import UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from forms import ProfileForm
from chat.models import ChatRoom


def profile(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'profiles/profile.html', context)    


def other_profile(request, slug):
    context = {}
    try:
        profile = Profile.objects.get(slug=slug)
        context['profile'] = profile
        context['friends'] = profile.get_friends()
        context['active_chats'] = ChatRoom.objects.filter(subscribers=profile)
        context['owned_chats'] = ChatRoom.objects.filter(owner=profile)
    except Profile.DoesNotExist:
        pass


    return render(request, 'profiles/other_profile.html', context)


class ProfileEdit(UpdateView):
    model = Profile
    template_name = 'profile_edit.html'
    form_class = ProfileForm

    fields = (
        'friends',
        'blocking')
    success_url = reverse_lazy('profile')


class ListProfiles(ListView):

    model = Profile
