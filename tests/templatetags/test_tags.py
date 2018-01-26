from django import template

from pattern_library.monkey_utils import override_tag

register = template.Library()


@register.simple_tag
def error_tag(arg=None):
    "Just raise an exception, never do anything"
    raise Exception("error_tag raised an exception")


override_tag(register, 'error_tag')
