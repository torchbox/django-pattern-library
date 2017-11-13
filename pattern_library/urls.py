from django.conf.urls import url

from pattern_library.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
