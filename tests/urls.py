from django.conf.urls import include, url

from pattern_library import urls as pattern_library_urls

urlpatterns = [
    url(r'^pattern-library/', include(pattern_library_urls)),
]
