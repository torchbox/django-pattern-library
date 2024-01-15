import inspect
import logging
import typing
import warnings

import django
from django.template.library import SimpleNode

from pattern_library.utils import is_pattern_library_context, render_pattern

logger = logging.getLogger(__name__)
UNSPECIFIED = object()


def override_tag(
    register: django.template.Library,
    name: str,
    default_html: typing.Optional[typing.Any] = UNSPECIFIED,
):
    """
    An utility that helps you override original tags for use in your pattern library.
    """

    original_tag = register.tags[name]

    @register.tag(name=name)
    def tag_func(parser, token):
        original_node = original_tag(parser, token)
        original_node_render = original_node.render

        def node_render(context):
            if is_pattern_library_context(context):
                tag_overridden = False
                result = ""

                # Get overridden tag config.
                tag_overrides = context.get("__pattern_library_tag_overrides", {})

                # Extract values for lookup from the token
                bits = token.split_contents()
                tag_name = bits[0]
                arguments = " ".join(bits[1:]).strip()

                # Get config for a specific tag
                tag_config = tag_overrides.get(tag_name, {})
                if tag_config:
                    # Get config for specific arguments
                    tag_config = tag_config.get(arguments, {})

                    if "raw" in tag_config:
                        # Return raw data (it can be string or a structure), if defined
                        result = tag_config["raw"]
                        tag_overridden = True
                    elif "template_name" in tag_config:
                        # Render pattern, if raw string is not defined
                        template_name = tag_config["template_name"]
                        request = context.get("request")
                        result = render_pattern(
                            request, template_name, allow_non_patterns=True
                        )
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
                        target_var = tag_config.get("target_var")

                    if target_var:
                        # If a value for the target_var is supplied,
                        # write result into the variable
                        context[target_var] = result
                        return ""

                    # Render result instead of the tag, as a string.
                    # See https://github.com/torchbox/django-pattern-library/issues/166.
                    return str(result)
                elif default_html is not UNSPECIFIED:
                    # Ensure default_html is a string.
                    if not isinstance(default_html, str):
                        # Save the caller for the override tag in case it's needed for error reporting.
                        trace = inspect.stack()[1]
                        if django.VERSION < (4, 0):
                            warnings.warn(
                                "default_html argument to override_tag should be a string to ensure compatibility "
                                'with Django >= 4.0 (line %s in "%s")'
                                % (trace.lineno, trace.filename),
                                Warning,
                            )
                        else:
                            raise TypeError(
                                'default_html argument to override_tag must be a string (line %s in "%s")'
                                % (trace.lineno, trace.filename)
                            )

                    # Render provided default;
                    # if no stub data supplied.
                    return default_html
                else:
                    logger.warning(
                        'No default or stub data defined for the "%s" tag in the "%s" template',
                        tag_name,
                        parser.origin.template_name,
                    )

            return original_node_render(context)

        original_node.render = node_render

        return original_node

    return tag_func
