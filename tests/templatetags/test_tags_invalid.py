from django import template

from pattern_library.monkey_utils import override_tag

register = template.Library()


@register.simple_tag()
def default_html_tag_invalid(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("default_tag raised an exception")


# Test overriding tag with a default_html that's not valid in Django >= 4.0
override_tag(register, "default_html_tag_invalid", default_html=[1, 2, 3])
