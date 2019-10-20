from django.conf.urls import url

from pattern_library import get_pattern_template_suffix, views

app_name = 'pattern_library'
urlpatterns = [
    # UI
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(
        r'^pattern/(?P<pattern_template_name>[\w./-]+%s)$' % (
            get_pattern_template_suffix()
        ),
        views.IndexView.as_view(),
        name='display_pattern'
    ),

    # iframe rendering
    url(
        r'^render-pattern/(?P<pattern_template_name>[\w./-]+%s)$' % (
            get_pattern_template_suffix()
        ),
        views.RenderPatternView.as_view(),
        name='render_pattern'
    ),
]
