from django.shortcuts import render, redirect
from models import Profile
from game_calendar.models import Event
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from chat.models import ChatRoom


@login_required
def profile(request):
    """
    View the user's own profile
    """
    profile = request.user.profile
    context = {
        'profile': profile,
        'events': Event.objects.filter(invitees=profile)
    }
    return render(request, 'profiles/profile.html', context)


@login_required
def other_profile(request, slug):
    """
    View another user's profile
    """
    context = {}
    if request.user.username == slug:
        return redirect(reverse("profile"))
    try:
        slug = slug.lower()
        profile = Profile.objects.get(slug=slug)
        context['profile'] = profile
        context['friends'] = profile.get_friends()
        context['active_chats'] = ChatRoom.objects.filter(subscribers=profile)
        context['owned_chats'] = ChatRoom.objects.filter(owner=profile)
    except Profile.DoesNotExist:
        return redirect(reverse('profile_list'))
    return render(request, 'profiles/other_profile.html', context)


@login_required
def make_friends(request, pk):
    """
    Request another user's friendship
    """
    request.user.profile.requested_friends.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')


@login_required
def add_friend(request, pk):
    """
    Adding two users as friends
    """
    prof = Profile.objects.get(pk=pk)
    request.user.profile.friends.add(prof)
    request.user.profile.requesting_friend.remove(prof)
    prof.requested_friends.remove(prof)
    return redirect('/profile/' + prof.user.username)


@login_required
def unfriend(request, pk):
    prof = Profile.objects.get(pk=pk)
    request.user.profile.unfriending(prof)
    return redirect('/profile/')


@login_required
def block_asshole(request, pk):
    """
    Blocking another user
    """
    request.user.profile.blocking.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')


@login_required
def unblock_asshole(request, pk):
    """
    Unblock another user that has been blocked
    """
    prof = Profile.objects.get(pk=pk)
    request.user.profile.blocking.remove(prof)
    return redirect('/profile/' + prof.user.username)


@login_required
def accept_invitation(request, pk):
    """
    Accepting an event set by another user
    """
    profile = request.user.profile
    event = Event.objects.get(pk=pk)
    event.attending.add(profile)
    event.invitees.remove(profile)
    return redirect('/calendar/')


@login_required
def deny_invitation(request, pk):
    profile = request.user.profile
    event = Event.objects.get(pk=pk)
    event.invitees.remove(profile)
    return redirect('/profile/')


class update_picture(UpdateView):
    """
    Update a user's profile picture
    """
    def get_context_data(self, *args, **kwargs):
        default = super(UpdateView, self).get_context_data(*args, **kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        try:
            default['picture_url'] = profile.picture.url
        except ValueError:
            pass
        return default

    def dispatch(self, request, *args, **kwargs):
        if int(self.kwargs['pk']) != self.request.user.profile.pk:
            return redirect('/accounts/login/')
        return super(update_picture, self).dispatch(request, *args, **kwargs)

    model = Profile
    template_name = 'profiles/update_picture.html'
    fields = ('picture',)
    success_url = reverse_lazy('profile')


class ListProfiles(ListView):
    """
    Listing all users that are registered
    """
    model = Profile
