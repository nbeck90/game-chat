from django.views.generic.dates import YearArchiveView

from game_calendar.models import Article

from django.shortcuts import render


class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True


def calendar(request, month, year):
    from calendar import HTMLCalendar
    from django.utils.safestring import mark_safe
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
                        body.append('<li>'+event.title+'</li>')
                    body.append('</ul>')
                    return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))

                return self.day_cell(cssclass, day)
            return self.day_cell('noday', '&nbsp;')

        def day_cell(self, cssclass, body):
            return '<td class="%s">%s</td>' % (cssclass, body)

    year, month = int(year), int(month)
    calendars = [mark_safe(SpecialCal().formatmonth(year, month))]
    for i in range(1, 6):
        month += 1
        if month > 12:
            year += 1
            month = 1
        calendars.append(mark_safe(SpecialCal().formatmonth(year, month)))

    from datetime import date, datetime, time, timedelta

    dt = datetime.combine(date.today(), time(23, 55)) + timedelta(minutes=30)


    return render(request,
                  'game_calendar/calendar.html',
                  {'calendars': calendars,
                   'articles': Article.objects.all()}
                  )
