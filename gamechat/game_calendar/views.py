from game_calendar.models import Article

from django.shortcuts import render


def return_event(request):
    from datetime import datetime
    from django.http import HttpResponse
    import json

    articles_list = Article.objects.all()
    json_list = []
    for article in articles_list:
        json_entry = {
            'title': article.title,
            'start': article.pub_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': False
            }
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')


def calendar(request, month, year):

    return render(request, 'game_calendar/calendar.html')
