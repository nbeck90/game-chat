from game_calendar.models import Article

from django.shortcuts import render


def day_detail(request, day, month, year):
    article_list = Article.objects.filter(pub_date__day=day).filter(pub_date__month=month).filter(pub_date__year=year)
    return render(request,
                  'game_calendar/day_detail.html',
                  {'article_list': article_list}
                  )


def event_detail(request, pk):

    article = Article.objects.get(pk=pk)
    return render(request,
                  'game_calendar/detail.html',
                  {'article': article}
                  )


def calendar(request, month, year):
    from django.utils.safestring import mark_safe

    year, month = int(year), int(month)
    calendars = [mark_safe(SpecialCal().formatmonth(year, month))]
    for i in range(1, 6):
        month += 1
        if month > 12:
            year += 1
            month = 1
        calendars.append(mark_safe(SpecialCal().formatmonth(year, month)))

    return render(request,
                  'game_calendar/calendar.html',
                  {'calendars': calendars,
                   'articles': Article.objects.all()}
                  )

from calendar import HTMLCalendar
from datetime import date


class SpecialCal(HTMLCalendar):

        def __init__(self):
            self.articles = Article.objects.all()
            super(SpecialCal, self).__init__()

        def formatmonth(self, year, month):
            self.year, self.month = year, month
            return super(SpecialCal, self).formatmonth(year, month)

        def formatday(self, day, weekday):

            if day != 0:
                cssclass = self.cssclasses[weekday]
                if date.today() == date(self.year, self.month, day):
                    cssclass += ' today'
                events = self.articles.filter(
                    pub_date__day=day).filter(pub_date__month=self.month)
                if len(events) > 0:
                    body = ['<ul>']
                    cssclass += ' filled'
                    for event in events:
                        pk = str(event.pk)
                        print pk
                        body.append('<a href="/calendar/event_detail/'+pk+'/">')
                        body.append('<li>'+event.title+'</li>')
                        body.append('</a>')
                    body.append('</ul>')
                    return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
                alink = "<a href='/calendar/%s/%s/%s/'>" % (day, self.month, self.year)
                day = alink+"%s</a>" % (day)
                print day
                return self.day_cell(cssclass, day)
            return self.day_cell('noday', '&nbsp;')

        def day_cell(self, cssclass, body):
            return '<td class="%s">%s</td>' % (cssclass, body)
