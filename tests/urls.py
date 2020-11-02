from django.conf import settings
from django.conf.urls import include, url

from pattern_library import urls as pattern_library_urls

if settings.GITHUB_PAGES_EXPORT:
    urlpatterns = [
        url(r'^django-pattern-library/demo/pattern-library/', include(pattern_library_urls)),
    ]
else:
    urlpatterns = [
        url(r'^pattern-library/', include(pattern_library_urls)),
    ]
