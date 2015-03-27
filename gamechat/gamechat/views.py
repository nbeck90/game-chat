from django.shortcuts import render


def home_page(request):
    ssb = ('/static/smash.jpg', 'Super Smash Brothers 4', 'chat/SSB4')
    wow = ('/static/wow.jpg', 'World of Warcraft', '/chat/WoW')
    lol = ('/static/lol.jpg', 'League of Legends', '/chat/LoL')
    csgo = ('/static/csgo.jpg', 'CS: Global Offensive', '/chat/CSGO')
    destiny = ('/static/destiny.jpg', 'Destiny', '/chat/Destiny')
    mine = ('/static/mine.jpg', 'Minecraft', '/chat/Minecraft')
    hearth = ('/static/hearth.jpg', 'Hearthstone', '/chat/Hearthstone')
    dota = ('/static/dota.jpg', 'Dota 2', '/chat/Dota2')
    diablo = ('/static/diablo.jpg', 'Diablo 3', '/chat/Diablo')
    local = ('/static/dnd.jpg', 'Local Gaming', '/chat/Local')

    games = [ssb, wow, lol, csgo, destiny, mine, hearth, dota, diablo, local]
    context = {}
    context['games'] = games
    return render(request, 'home.html', context)


def four_o_four(request):
    ssb = ('/static/smash.jpg', 'Super Smash Brothers 4', 'chat/SSB4')
    wow = ('/static/wow.jpg', 'World of Warcraft', '/chat/WoW')
    lol = ('/static/lol.jpg', 'League of Legends', '/chat/LoL')
    csgo = ('/static/csgo.jpg', 'CS: Global Offensive', '/chat/CSGO')
    destiny = ('/static/destiny.jpg', 'Destiny', '/chat/Destiny')
    mine = ('/static/mine.jpg', 'Minecraft', '/chat/Minecraft')
    hearth = ('/static/hearth.jpg', 'Hearthstone', '/chat/Hearthstone')
    dota = ('/static/dota.jpg', 'Dota 2', '/chat/Dota2')
    diablo = ('/static/diablo.jpg', 'Diablo 3', '/chat/Diablo')
    local = ('/static/dnd.jpg', 'Local Gaming', '/chat/Local')

    games = [ssb, wow, lol, csgo, destiny, mine, hearth, dota, diablo, local]
    context = {}
    context['games'] = games
    return render(request, 'four.html', context)
