import os
import re
from collections import OrderedDict

from django.apps import apps
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from django.template.loaders.app_directories import get_app_template_dirs
from django.utils.safestring import mark_safe

import markdown
import yaml

from pattern_library import (
    get_pattern_context_var_name, get_pattern_template_dir,
    get_pattern_template_prefix, get_pattern_template_suffix
)
from pattern_library.exceptions import TemplateIsNotPattern


def is_pattern(template_name):
    return template_name.endswith(get_pattern_template_suffix())


def is_pattern_type(template_name, pattern_type):
    if not is_pattern(template_name):
        return False

    substring = '/{}/'.format(pattern_type)
    return substring in template_name


def is_pattern_library_context(context):
    context_var_name = get_pattern_context_var_name()

    return context.get(context_var_name) is True


def base_dict():
    return {'templates_stored': [], 'template_groups': {}}


def get_pattern_templates():
    templates = base_dict()
    template_dirs = get_app_template_dirs('templates')

    for lookup_dir in template_dirs:
        app_folder = lookup_dir.split(os.sep)[-2]
        try:
            app_name = apps.get_app_config(app_folder).verbose_name
        except LookupError:
            app_name = app_folder.title()

        for root, dirs, files in os.walk(lookup_dir, topdown=True):
            # Ignore folders without files
            if not files:
                continue

            found_templates = []
            for current_file in files:
                pattern_path = os.path.join(root, current_file)
                pattern_path = os.path.relpath(pattern_path, lookup_dir)

                if is_pattern(pattern_path):
                    template = get_template(pattern_path)
                    pattern_config = get_pattern_config(pattern_path)
                    pattern_name = pattern_config.get('name')
                    if pattern_name:
                        template.pattern_name = pattern_name
                    found_templates.append(template)

            sub_folders = os.path.relpath(root, lookup_dir)
            if found_templates:
                templates_to_store = templates
                for folder in [app_name, *sub_folders.split(os.sep)]:
                    try:
                        templates_to_store = templates_to_store['template_groups'][folder]
                    except KeyError:
                        templates_to_store['template_groups'][folder] = base_dict()
                        templates_to_store = templates_to_store['template_groups'][folder]

                templates_to_store['templates_stored'].extend(found_templates)
    return templates


def get_pattern_config_str(template_name):
    replace_pattern = '{}$'.format(get_pattern_template_suffix())
    context_file = re.sub(replace_pattern, '', template_name)

    context_file = context_file + '.yaml'
    context_file = os.path.join(get_pattern_template_dir(), context_file)

    try:
        # Default encoding is platform-dependant, so we explicitly open it as utf-8.
        with open(context_file, 'r', encoding='utf-8') as f:
            return str(f.read())
    except IOError:
        return ''


def get_pattern_config(template_name):
    config_str = get_pattern_config_str(template_name)
    if config_str:
        return yaml.load(config_str, Loader=yaml.FullLoader)
    return {}


def mark_context_strings_safe(value, parent=None, subscript=None):
    if isinstance(value, list):
        for index, sub_value in enumerate(value):
            mark_context_strings_safe(sub_value, parent=value, subscript=index)

    elif isinstance(value, dict):
        for key, sub_value in value.items():
            mark_context_strings_safe(sub_value, parent=value, subscript=key)

    elif isinstance(value, str):
        parent[subscript] = mark_safe(value)


def get_pattern_context(template_name):
    config = get_pattern_config(template_name)
    context = config.get('context', {})

    mark_context_strings_safe(context)

    return context


def get_pattern_markdown(template_name):
    replace_pattern = '{}$'.format(get_pattern_template_suffix())
    md_file = re.sub(replace_pattern, '', template_name)

    md_file = md_file + '.md'
    md_file = os.path.join(get_pattern_template_dir(), md_file)

    try:
        # Default encoding is platform-dependant, so we explicitly open it as utf-8.
        with open(md_file, 'r', encoding='utf-8') as f:
            htmlmarkdown = markdown.markdown(f.read())
            return htmlmarkdown
    except IOError:
        return ''


def render_pattern(request, template_name):
    if not is_pattern(template_name):
        raise TemplateIsNotPattern

    context = get_pattern_context(template_name)
    context[get_pattern_context_var_name()] = True
    return render_to_string(template_name, request=request, context=context)
