from django.shortcuts import render, redirect
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
    if request.user.username == slug:
        return redirect("/profile/")
    try:
        profile = Profile.objects.get(slug=slug)
        context['profile'] = profile
        context['friends'] = profile.get_friends()
        context['active_chats'] = ChatRoom.objects.filter(subscribers=profile)
        context['owned_chats'] = ChatRoom.objects.filter(owner=profile)
    except Profile.DoesNotExist:
        pass

    return render(request, 'profiles/other_profile.html', context)


def make_friends(request, pk):
    request.user.profile.requested_friends.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')


def add_friend(request, pk):
    prof = Profile.objects.get(pk=pk)
    request.user.profile.friends.add(prof)
    request.user.profile.requesting_friend.remove(prof)
    return redirect('/profile/'+prof.user.username)


def block_asshole(request, pk):
    request.user.profile.blocking.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')


def unblock_asshole(request, pk):
    prof = Profile.objects.get(pk=pk)
    request.user.profile.blocking.remove(prof)
    return redirect('/profile/'+prof.user.username)


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
