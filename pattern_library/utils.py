import operator
import os
import re

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.context import Context
from django.template.loader import get_template, render_to_string
from django.template.loader_tags import ExtendsNode
from django.template.loaders.app_directories import get_app_template_dirs
from django.utils.safestring import mark_safe

import markdown
import yaml
import pathlib
from pathlib import Path

from pattern_library import (
    get_pattern_context_var_name,
    get_pattern_template_suffix,
    get_sections,
)
from pattern_library.context_modifiers import registry
from pattern_library.exceptions import TemplateIsNotPattern



from django.utils.html import escape

def path_to_section():
    section_config = get_sections()
    sections = {}
    for section, paths in section_config:
        for path in paths:
            sections[Path(path)] = section
    return sections


def is_pattern(template_name):
    if not str(template_name).endswith(get_pattern_template_suffix()):
        return False

    section, path = section_for(os.path.dirname(template_name))
    if section is None:
        return False

    return True


def is_pattern_library_context(context):
    context_var_name = get_pattern_context_var_name()

    return context.get(context_var_name) is True


def section_for(template_folder):
    paths = path_to_section()
    for path in paths:
        if str(template_folder).startswith(str(path)):
            return paths[path], path
    return None, None


def base_dict():
    return {"templates_stored": [], "template_groups": {}}


def order_dict(dictionary, key_sort=None):
    # Order a dictionary by the keys
    values = list(dictionary.items())
    if not key_sort:
        values.sort(key=operator.itemgetter(0))
    else:
        values.sort(key=lambda key: key_sort(key[0]))
    return dict(values)


def get_template_dirs():
    template_dirs = [
        d for engines in settings.TEMPLATES for d in engines.get("DIRS", [])
    ]
    template_app_dirs = get_app_template_dirs("templates")
    template_dirs += template_app_dirs
    return template_dirs


def get_pattern_config_str(template_name):
    replace_pattern = "{}$".format(get_pattern_template_suffix())
    context_path = re.sub(replace_pattern, "", template_name)

    context_name = context_path + ".yaml"
    try:
        context_file = get_template(context_name)
    except TemplateDoesNotExist:
        context_name = context_path + ".yml"
        try:
            context_file = get_template(context_name)
        except TemplateDoesNotExist:
            return ""

    return context_file.render()


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
    context = config.get("context", {})

    mark_context_strings_safe(context)

    return context


def get_pattern_markdown(template_name):
    replace_pattern = "{}$".format(get_pattern_template_suffix())
    md_path = re.sub(replace_pattern, "", template_name)

    md_name = md_path + ".md"
    try:
        md_file = get_template(md_name)
    except TemplateDoesNotExist:
        return ""

    with open(md_file.origin.name, "r", encoding="utf-8") as f:
        return markdown.markdown(f.read())


def render_pattern(request, template_name, allow_non_patterns=False, config=None):
    if not allow_non_patterns and not is_pattern(template_name):
        raise TemplateIsNotPattern

    if not config:
        config = get_pattern_config(template_name)

    context = config.get("context", {})
    tags = config.get("tags", {})
    mark_context_strings_safe(context)
    context[get_pattern_context_var_name()] = True
    context["__pattern_library_tag_overrides"] = tags
    for modifier in registry.get_for_template(template_name):
        modifier(context=context, request=request)
    return render_to_string(template_name, request=request, context=context)


def get_renderer():
    return TemplateRenderer


class TemplateRenderer:
    @classmethod
    def get_pattern_templates(cls):
        templates = base_dict()
        template_dirs = get_template_dirs()

        for lookup_dir in template_dirs:
            for root, dirs, files in os.walk(lookup_dir, topdown=True):
                # Ignore folders without files
                if not files:
                    continue

                base_path = os.path.relpath(root, lookup_dir)
                section, path = section_for(Path(base_path))

                # It has no section, ignore it
                if not section:
                    continue

                found_templates = []
                for current_file in files:
                    pattern_path = Path(root) / Path(current_file)
                    pattern_path = Path(pattern_path.relative_to(lookup_dir))

                    if is_pattern(pattern_path):
                        template = get_template(pattern_path)
                        pattern_config = get_pattern_config(pattern_path)
                        pattern_name = pattern_config.get("name")
                        pattern_filename = Path(template.origin.template_name).relative_to(base_path)

                        if pattern_name:
                            template.pattern_name = pattern_name
                        else:
                            template.pattern_name = pattern_filename

                        template.pattern_filename = pattern_filename

                        found_templates.append(template)

                if found_templates:
                    lookup_dir_relpath = Path(root).relative_to(lookup_dir)
                    sub_folders = Path(lookup_dir_relpath).relative_to(path)
                    templates_to_store = templates
                    for folder in [section, *str(sub_folders).split(os.sep)]:
                        try:
                            templates_to_store = templates_to_store["template_groups"][
                                folder
                            ]
                        except KeyError:
                            templates_to_store["template_groups"][folder] = base_dict()

                            templates_to_store = templates_to_store["template_groups"][
                                folder
                            ]

                    templates_to_store["templates_stored"].extend(found_templates)

        # Order the templates alphabetically
        for templates_objs in templates["template_groups"].values():
            templates_objs["template_groups"] = order_dict(
                templates_objs["template_groups"]
            )

        # Order the top level by the sections
        section_order = [section for section, _ in get_sections()]
        templates["template_groups"] = order_dict(
            templates["template_groups"], key_sort=lambda key: section_order.index(key)
        )

        return templates

    @classmethod
    def get_pattern_source(cls, template):
        return cls._get_engine(template).get_pattern_source(template)

    @classmethod
    def get_template_ancestors(cls, template_name, context=None):
        template = get_template(template_name)
        return cls._get_engine(template).get_template_ancestors(template_name, context=context)

    @classmethod
    def _get_engine(cls, template):
        if "jinja" in str(type(template)).lower():
            return JinjaTemplateRenderer
        return DTLTemplateRenderer

class DTLTemplateRenderer:
    @staticmethod
    def get_pattern_source(template):
        return escape(template.template.source)

    @classmethod
    def get_template_ancestors(cls, template_name, context=None, ancestors=None):
        """
        Returns a list of template names, starting with provided name
        and followed by the names of any templates that extends until
        the most extended template is reached.
        """
        if ancestors is None:
            ancestors = [template_name]

        if context is None:
            context = Context()

        pattern_template = get_template(template_name)

        for node in pattern_template.template.nodelist:
            if isinstance(node, ExtendsNode):
                parent_template_name = node.parent_name.resolve(context)
                ancestors.append(parent_template_name)
                cls.get_template_ancestors(
                    parent_template_name, context=context, ancestors=ancestors
                )
                break

        return ancestors


class JinjaTemplateRenderer:
    @staticmethod
    def get_pattern_source(template):
        with open(template.template.filename) as f:
            source =  escape(f.read())
        return source

    @classmethod
    def get_template_ancestors(cls, template_name, context=None, ancestors=None):
        """
        Returns a list of template names, starting with provided name
        and followed by the names of any templates that extends until
        the most extended template is reached.
        """
        from jinja2.nodes import Extends

        if ancestors is None:
            ancestors = [template_name]

        if context is None:
            context = Context()

        pattern_template = get_template(template_name)
        #todo - make sure envrionment has context passed in
        environment = pattern_template.template.environment
        nodelist = environment.parse(pattern_template.name)
        parent_template_name = nodelist.find(Extends)
        if parent_template_name:
            ancestors.append(parent_template_name)
            cls.get_template_ancestors(parent_template_name, context=context, ancestors=ancestors)

        return ancestors
