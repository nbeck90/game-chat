from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required
from game_calendar.views import ArticleYearArchiveView

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/$',
        ArticleYearArchiveView.as_view(
            template_name="game_calendar/article_archive_year.html"
            ),
        name="article_year_archive"),
    url(r'^(?P<month>\d{2})/(?P<year>\d{4})/$', views.calendar, name='calendar_view'),
    url(r'^event_detail/(?P<pk>\d+)/$', views.event_detail, name='event_detail')
)
