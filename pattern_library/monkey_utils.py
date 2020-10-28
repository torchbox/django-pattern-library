import logging

from django.template.library import SimpleNode

from pattern_library.utils import (
    get_pattern_config, is_pattern_library_context, render_pattern
)

logger = logging.getLogger(__name__)
UNSPECIFIED = object()


def override_tag(register, name, default_html=None):
    """
    An utility that helps you override original tags for use in your pattern library.

    Accepts the register argument which should be an instance of django.template.Library.
    """

    original_tag = register.tags[name]

    @register.tag(name=name)
    def tag_func(parser, token):
        original_node = original_tag(parser, token)
        original_node_render = original_node.render

        def node_render(context):
            if is_pattern_library_context(context):
                tag_overridden = False
                result = ''

                # Load pattern's config
                current_template_name = parser.origin.template_name
                pattern_config = get_pattern_config(current_template_name)

                # Extract values for lookup from the token
                bits = token.split_contents()
                tag_name = bits[0]
                arguments = ' '.join(bits[1:]).strip()

                # Get config for a specific tag
                tag_config = pattern_config.get('tags', {}).get(tag_name, {})
                if tag_config:
                    # Get config for specific arguments
                    tag_config = tag_config.get(arguments, {})

                    if 'raw' in tag_config:
                        # Return raw data (it can be string or a structure), if defined
                        result = tag_config['raw']
                        tag_overridden = True
                    elif 'template_name' in tag_config:
                        # Render pattern, if raw string is not defined
                        template_name = tag_config['template_name']
                        request = context.get('request')
                        result = render_pattern(request, template_name, allow_non_patterns=True)
                        tag_overridden = True

                    # TODO: Allow objects with the __str__ method
                    # In some cases we must return an object that can
                    # be rendered as a string `{{ result }}`
                    # and allow users to access it's attributes `{{ result.url }}`

                if tag_overridden:
                    if isinstance(original_node, SimpleNode):
                        # If it's a SimpleNode try to use it's target_var
                        target_var = original_node.target_var
                    else:
                        # If it's a custom tag, check for the target_var in tag's config
                        target_var = tag_config.get('target_var')

                    if target_var:
                        # If a value for the target_var is supplied,
                        # write result into the variable
                        context[target_var] = result
                        return ''

                    # Render result instead of the tag
                    return result
                elif default_html is not UNSPECIFIED:
                    # Render provided default;
                    # if no stub data supplied.
                    return default_html
                else:
                    logger.warning(
                        'No default or stub data defined for the "%s" tag in the "%s" template',
                        tag_name, current_template_name
                    )

            return original_node_render(context)

        original_node.render = node_render

        return original_node

    return tag_func
