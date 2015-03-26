from django.shortcuts import render


def home_page(request):
    ssb = ('/static/smash.jpg', 'Super Smash Brothers 4', 'chat/ssb')
    wow = ('/static/wow.jpg', 'World of Warcraft', '/chat/wow')
    lol = ('/static/lol.jpg', 'League of Legends', '/chat/lol')
    csgo = ('/static/csgo.jpg', 'CS: Global Offensive', '/chat/cs')
    destiny = ('/static/destiny.jpg', 'Destiny', '/chat/destiny')
    mine = ('/static/mine.jpg', 'Minecraft', '/chat/mine')
    hearth = ('/static/hearth.jpg', 'Hearthstone', '/chat/hearth')
    dota = ('/static/dota.jpg', 'Dota 2', '/chat/dota')
    diablo = ('/static/diablo.jpg', 'Diablo 3', '/chat/diablo')
    local = ('/static/dnd.jpg', 'Local Gaming', '/chat/local')

    games = [ssb, wow, lol, csgo, destiny, mine, hearth, dota, diablo, local]
    context = {}
    context['games'] = games
    return render(request, 'home.html', context)
