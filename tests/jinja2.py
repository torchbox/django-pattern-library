from django.apps import apps
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.context_processors import csrf
from django.template.defaultfilters import (
    cut,
    date,
    linebreaks,
    pluralize,
    slugify,
    truncatewords,
    urlencode,
)
from django.urls import reverse

from jinja2 import Environment

from pattern_library.monkey_utils import override_jinja_tags

if apps.is_installed("pattern_library"):
    override_jinja_tags()


def error_tag():
    "Just raise an exception, never do anything"
    raise Exception("error_tag raised an exception")


def pageurl(page):
    """Approximation of wagtail built-in tag for realistic example."""
    return "/page/url"


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
            "csrf": csrf,
            "error_tag": error_tag,
            "pageurl": pageurl,
        }
    )
    env.filters.update(
        {
            "cut": cut,
            "date": date,
            "linebreaks": linebreaks,
            "pluralize": pluralize,
            "slugify": slugify,
            "truncatewords": truncatewords,
            "urlencode": urlencode,
        }
    )
    return env
