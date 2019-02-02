from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.utils.html import escape
from django.views.generic.base import TemplateView

from pattern_library import get_pattern_base_template_name, get_pattern_types
from pattern_library.exceptions import (
    PatternLibraryEmpty, TemplateIsNotPattern
)
from pattern_library.utils import (
    get_pattern_config, get_pattern_config_str, get_pattern_template_dir,
    get_pattern_templates, is_pattern_type, render_pattern
)


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get_first_template(self, templates):
        for pattern_type in templates:
            pattern_groups = templates[pattern_type]
            for pattern_group in pattern_groups:
                pattern_templates = pattern_groups[pattern_group]
                for pattern_template in pattern_templates:
                    return pattern_template.origin.template_name

        raise PatternLibraryEmpty(
            "No templates found in the pattern library at '%s'"
            % get_pattern_template_dir()
        )

    def get(self, request, pattern_template_name=None):
        # Get all pattern templates
        available_pattern_types = get_pattern_types()
        templates = get_pattern_templates(available_pattern_types)

        if pattern_template_name is None:
            # Just display the first pattern if a specific one isn't requested
            pattern_template_name = self.get_first_template(templates)

        template = get_template(pattern_template_name)
        pattern_config = get_pattern_config(pattern_template_name)

        context = self.get_context_data()
        context['pattern_templates'] = templates
        context['pattern_template_name'] = pattern_template_name
        context['pattern_source'] = escape(template.template.source)
        context['pattern_config'] = escape(get_pattern_config_str(pattern_template_name))
        context['pattern_name'] = pattern_config.get('name', pattern_template_name)

        return self.render_to_response(context)


class RenderPatternView(TemplateView):
    http_method_names = ('get',)
    template_name = get_pattern_base_template_name()

    def get(self, request, pattern_template_name=None):
        try:
            rendered_pattern = render_pattern(request, pattern_template_name)
        except TemplateIsNotPattern:
            return HttpResponseBadRequest()

        # Do not render page patterns as part of the base template
        # because it should already extend base template
        if is_pattern_type(pattern_template_name, 'pages'):
            return HttpResponse(rendered_pattern)

        context = self.get_context_data()
        context['pattern_library_rendered_pattern'] = rendered_pattern

        return self.render_to_response(context)
