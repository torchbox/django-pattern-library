from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from pattern_library import get_setting
import os

register = template.Library()


@register.simple_tag
def pattern_library_custom_css():
    """
    Include custom CSS file for pattern library customization.

    This tag reads the CUSTOM_CSS setting from PATTERN_LIBRARY and includes
    the CSS file as a <link> tag. The CSS file should contain CSS custom properties
    that override the default pattern library styles.

    Usage in templates:
        {% load pattern_library_tags %}
        {% pattern_library_custom_css %}

    Example PATTERN_LIBRARY setting:
        PATTERN_LIBRARY = {
            "CUSTOM_CSS": "css/pattern-library-custom.css"  # relative to STATIC_URL
        }

    Example custom CSS file content:
        :root {
            --color-primary: #ff6b6b;
            --family-primary: 'Custom Font', sans-serif;
            --site-title: 'My Custom Library';
        }
    """
    custom_css_path = get_setting('CUSTOM_CSS')

    if not custom_css_path:
        return ''

    # Generate static URL for the CSS file
    try:
        css_url = static(custom_css_path)
        return mark_safe(f'<link rel="stylesheet" type="text/css" href="{css_url}">')
    except Exception:
        # If static file handling fails, return empty string
        return ''