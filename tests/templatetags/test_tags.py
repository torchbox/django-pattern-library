from django import template

from pattern_library.monkey_utils import override_tag

register = template.Library()

# Basic template tag
@register.simple_tag
def error_tag(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("error_tag raised an exception")

# Template tag to to test setting a default.
@register.simple_tag()
def default_tag(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("default_tag raised an exception")


override_tag(register, 'default_tag', default="https://potato.com")
override_tag(register, 'error_tag')
