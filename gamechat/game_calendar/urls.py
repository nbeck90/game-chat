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
)