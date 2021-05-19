from django.urls import re_path

from pattern_library import get_pattern_template_suffix, views

app_name = 'pattern_library'
urlpatterns = [
    # UI
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(
        r'^pattern/(?P<pattern_template_name>[\w./-]+%s)$' % (
            get_pattern_template_suffix()
        ),
        views.IndexView.as_view(),
        name='display_pattern'
    ),

    # iframe rendering
    re_path(
        r'^render-pattern/(?P<pattern_template_name>[\w./-]+%s)$' % (
            get_pattern_template_suffix()
        ),
        views.RenderPatternView.as_view(),
        name='render_pattern'
    ),
]
