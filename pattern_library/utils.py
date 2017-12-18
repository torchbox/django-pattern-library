import os
import re
from collections import OrderedDict

from django.template import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string

import yaml

from pattern_library import (
    get_pattern_context_var_name, get_pattern_template_dir,
    get_pattern_template_prefix, get_pattern_template_suffix
)
from pattern_library.exceptions import TemplateIsNotPattern


def is_pattern(template_name):
    return (
        template_name.startswith(get_pattern_template_prefix()) and
        template_name.endswith(get_pattern_template_suffix())
    )


def is_pattern_type(template_name, pattern_type):
    if not is_pattern(template_name):
        return False

    substring = '/{}/'.format(pattern_type)
    return substring in template_name


def is_pattern_library_context(context):
    context_var_name = get_pattern_context_var_name()

    return context.get(context_var_name) is True


def get_pattern_templates(pattern_types):
    templates = OrderedDict()

    base_lookup_dir = get_pattern_template_dir()
    lookup_dir = os.path.join(base_lookup_dir, get_pattern_template_prefix())

    for pattern_type in pattern_types:
        # We can't use defaultdict here, because Django templates
        # can't handle it properly: Django will try to resolve `templates.items`
        # as `templates['items']` not as `templates.items()`
        templates.setdefault(pattern_type, {})
        pattern_type_path = os.path.join(lookup_dir, pattern_type)

        for root, dirs, files in os.walk(pattern_type_path):
            # Do not allow patterns to sit directly underneath the pattern_type_path dir
            if root == pattern_type_path:
                continue

            # Ignore folders without files
            if not files:
                continue

            pattern_subtype = os.path.relpath(root, pattern_type_path)
            templates[pattern_type].setdefault(pattern_subtype, [])

            for current_file in files:
                pattern_path = os.path.join(root, current_file)
                pattern_path = os.path.relpath(pattern_path, base_lookup_dir)

                # Include only pattern templates
                if is_pattern(pattern_path):
                    try:
                        templates[pattern_type][pattern_subtype].append(
                            get_template(pattern_path)
                        )
                    except TemplateDoesNotExist:
                        pass

    return templates


# TODO: Implement cache (should, probably work on per-request basis for easier development)
def get_pattern_config(template_name):
    replace_pattern = '{}$'.format(get_pattern_template_suffix())
    context_file = re.sub(replace_pattern, '', template_name)

    context_file = context_file + '.yaml'
    context_file = os.path.join(get_pattern_template_dir(), context_file)

    context = {}
    try:
        with open(context_file, 'r') as f:
            context = yaml.load(f)
    except IOError:
        # It's possible that pattern has no data related
        pass

    return context


def get_pattern_context(template_name):
    config = get_pattern_config(template_name)

    return config.get('context', {})


def render_pattern(request, template_name):
    if not is_pattern(template_name):
        raise TemplateIsNotPattern

    context = get_pattern_context(template_name)
    context[get_pattern_context_var_name()] = True
    return render_to_string(template_name, request=request, context=context)