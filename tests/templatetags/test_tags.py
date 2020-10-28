from django import template

from pattern_library.monkey_utils import override_tag

register = template.Library()


# Basic template tag
@register.simple_tag
def error_tag(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("error_tag raised an exception")


# Template tag to to test setting a default html value.
@register.simple_tag()
def default_html_tag(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("default_tag raised an exception")


# Template tag to to test setting a default html value that is falsey.
@register.simple_tag()
def default_html_tag_falsey(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("default_tag raised an exception")


override_tag(register, 'error_tag')
override_tag(register, 'default_html_tag', default_html="https://potato.com")
override_tag(register, 'default_html_tag_falsey', default_html=None)
