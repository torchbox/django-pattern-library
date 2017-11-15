from django.template import Library
from django.template.loader_tags import (
    construct_relative_path,
    IncludeNode as DjangoIncludeNode
)

from django.template.base import TemplateSyntaxError, token_kwargs

from pattern_library.utils import get_context_for_template

register = Library()

# TODO: override {% extends %} and {% block %} tags


class IncludeNode(DjangoIncludeNode):
    """
    A copy of Django's IncludeNode that injects context from a file.
    """

    def render(self, context):
        if context.get('__pattern_library_view'):
            context.update(
                get_context_for_template(self.template.var)
            )

        return super().render(context)


@register.tag('include')
def do_include(parser, token):
    """
    Copy if Django's built-in {% include ... %} tag that uses the custom
    IncludeNode to allow us to
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )
    options = {}
    remaining_bits = bits[2:]
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    return IncludeNode(parser.compile_filter(bits[1]), extra_context=namemap,
                       isolated_context=isolated_context)
