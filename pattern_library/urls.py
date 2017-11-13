from django.conf.urls import url

from pattern_library.views import IndexView

app_name = 'pattern_library'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
