from django.shortcuts import render, redirect
from models import Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.core.urlresolvers import reverse_lazy
from forms import ProfileForm
from chat.models import ChatRoom

@login_required
def profile(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'profiles/profile.html', context)    

@login_required
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

@login_required
def make_friends(request, pk):
    request.user.profile.requested_friends.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')

@login_required
def add_friend(request, pk):
    prof = Profile.objects.get(pk=pk)
    request.user.profile.friends.add(prof)
    request.user.profile.requesting_friend.remove(prof)
    prof.requested_friends.remove(prof)
    return redirect('/profile/'+prof.user.username)

@login_required
def block_asshole(request, pk):
    request.user.profile.blocking.add(Profile.objects.get(pk=pk))
    return redirect('/profile/')

@login_required
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
