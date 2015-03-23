from django.shortcuts import render

def profile(request):
    profile = request.user.profile
    friends = profile.get_friends()
    context = {'profile': profile,
               'friends': friends}
    return render(request, 'profiles/profile.html', context)
