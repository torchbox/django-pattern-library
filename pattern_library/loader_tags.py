from django.template import ContextPopException, Library
from django.template.base import TemplateSyntaxError, token_kwargs
from django.template.loader_tags import ExtendsNode as DjangoExtendsNode
from django.template.loader_tags import IncludeNode as DjangoIncludeNode
from django.template.loader_tags import construct_relative_path

from pattern_library.utils import (
    get_pattern_context, is_pattern_library_context
)

register = Library()


class ExtendsNode(DjangoExtendsNode):
    """
    A copy of Django's ExtendsNode that injects context from a file.
    """
    def render(self, context):
        if is_pattern_library_context(context):
            parent_name = self.parent_name.resolve(context)
            parent_context = get_pattern_context(parent_name)
            if parent_context:
                # We want parent_context to appear later in the lookup process
                # than context of the actual template.
                # So we push parent_context into the beginning of the context stack.
                # See https://docs.djangoproject.com/en/1.11/ref/templates/api/#playing-with-context-objects
                pop_dicts = []
                try:
                    while True:
                        pop_dicts.append(context.pop())
                except ContextPopException:
                    pass

                context.push(parent_context)

                for pop_dict in reversed(pop_dicts):
                    context.push(pop_dict)

        return super().render(context)


def merge_pattern_context(context, pattern_context):
    # pattern_context is the included pattern's context from YAML
    # context is the context from the template containing the include tag

    # Looping over keys in pattern_context:
    #  - If a key is present in context and both values are dicts,
    #    update the pattern_context value with the context value
    for key, value in pattern_context.items():
        if key in context:
            parent_value = context[key]
            if isinstance(parent_value, dict) and isinstance(value, dict):
                value.update(parent_value)
            # TODO: Recursion? Apply similar logic to parent_value and value


class IncludeNode(DjangoIncludeNode):
    """
    A copy of Django's IncludeNode that injects context from a file.
    """
    def render(self, context):
        if is_pattern_library_context(context):
            template = self.template.resolve(context)
            pattern_context = get_pattern_context(template)
            extra_context = {name: var.resolve(context) for name, var in self.extra_context.items()}

            if self.isolated_context:
                context = context.new()

            merge_pattern_context(context, pattern_context)

            with context.push(pattern_context):
                with context.push(extra_context):
                    original_extra_context = self.extra_context
                    original_isolated_context = self.isolated_context

                    # Force superclass to render with the exact context we've provided.
                    self.extra_context = {}
                    self.isolated_context = False
                    output = super().render(context)

                    # Restore original context variables (nodes are rendered repeatedly inside for loops etc.)
                    self.extra_context = original_extra_context
                    self.isolated_context = original_isolated_context

                    return output

        return super().render(context)


@register.tag('extends')
def do_extends(parser, token):
    """
    A copy of Django's built-in {% extends ... %} tag that uses our custom
    ExtendsNode to allow us to load dummy context for the pattern library.
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes one argument" % bits[0])
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    parent_name = parser.compile_filter(bits[1])
    nodelist = parser.parse()
    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])
    return ExtendsNode(nodelist, parent_name)


@register.tag('include')
def do_include(parser, token):
    """
    A copy of Django's built-in {% include ... %} tag that uses our custom
    IncludeNode to allow us to load dummy context for the pattern library.
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
