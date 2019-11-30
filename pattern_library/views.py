from django.http import Http404
from django.template.loader import get_template
from django.utils.html import escape
from django.views.generic.base import TemplateView

from pattern_library import get_pattern_base_template_name
from pattern_library.exceptions import (
    PatternLibraryEmpty, TemplateIsNotPattern
)
from pattern_library.utils import (
    get_pattern_config, get_pattern_config_str, get_pattern_markdown,
    get_pattern_templates, get_sections, is_pattern, render_pattern
)


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def first_template_from_group(self, templates):
        try:
            return templates['templates_stored'][0]
        except IndexError:
            for template_group in templates['template_groups'].values():
                return self.first_template_from_group(template_group)
        return None

    def get_first_template(self, templates):
        first_template = self.first_template_from_group(templates)
        if first_template:
            return first_template.origin.template_name

        sections = get_sections()
        if sections:
            raise PatternLibraryEmpty(
                "No templates found matching: '%s'"
                % str(sections)
            )
        else:
            raise PatternLibraryEmpty(
                "No 'SECTIONS' found in the 'PATTERN_LIBRARY' setting"
            )

    def get(self, request, pattern_template_name=None):
        # Get all pattern templates
        templates = get_pattern_templates()

        if pattern_template_name is None:
            # Just display the first pattern if a specific one isn't requested
            pattern_template_name = self.get_first_template(templates)

        if not is_pattern(pattern_template_name):
            raise Http404

        template = get_template(pattern_template_name)
        pattern_config = get_pattern_config(pattern_template_name)

        context = self.get_context_data()
        context['pattern_templates'] = templates
        context['pattern_template_name'] = pattern_template_name
        context['pattern_source'] = escape(template.template.source)
        context['pattern_config'] = escape(get_pattern_config_str(pattern_template_name))
        context['pattern_name'] = pattern_config.get('name', pattern_template_name)
        context['pattern_markdown'] = get_pattern_markdown(pattern_template_name)

        return self.render_to_response(context)


class RenderPatternView(TemplateView):
    http_method_names = ('get',)
    template_name = get_pattern_base_template_name()

    def get(self, request, pattern_template_name=None):
        try:
            rendered_pattern = render_pattern(request, pattern_template_name)
        except TemplateIsNotPattern:
            raise Http404

        context = self.get_context_data()
        context['pattern_library_rendered_pattern'] = rendered_pattern

        return self.render_to_response(context)
