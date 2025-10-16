from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from pattern_library import get_setting

register = template.Library()


@register.simple_tag
def pattern_library_custom_css():
    """
    Include custom CSS for pattern library customization.

    This tag optionally includes an external CSS file for additional customization.

    Usage in templates:
        {% load pattern_library_tags %}
        {% pattern_library_custom_css %}

    Example PATTERN_LIBRARY setting:
        PATTERN_LIBRARY = {
            "CUSTOM_CSS": "css/pattern-library-custom.css"  # relative to STATIC_URL
        }
    """
    css_content = []

    # Include external CSS file if specified
    custom_css_path = get_setting("CUSTOM_CSS")
    if custom_css_path:
        try:
            css_url = static(custom_css_path)
            css_content.append(
                f'<link rel="stylesheet" type="text/css" href="{css_url}">'
            )
        except Exception:
            pass  # If static file handling fails, just skip the external file

    return mark_safe("\n".join(css_content))


@register.simple_tag
def pattern_library_site_title():
    """
    Get the site title for the pattern library.

    Usage in templates:
        {% load pattern_library_tags %}
        {% pattern_library_site_title %}
    """
    return get_setting("SITE_TITLE")
