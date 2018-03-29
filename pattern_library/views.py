from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView

from pattern_library import get_pattern_base_template_name, get_pattern_types
from pattern_library.exceptions import TemplateIsNotPattern
from pattern_library.utils import (
    get_pattern_templates, is_pattern_type, render_pattern, render_pattern_listing
)


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get(self, request, template_name=None):
        # Get all pattern templates
        available_pattern_types = get_pattern_types()
        templates = get_pattern_templates(available_pattern_types)

        if template_name is None:
            # Just display the first pattern if a specific one isn't requested
            for pattern_type in templates:
                pattern_groups = templates[pattern_type]
                for pattern_group in pattern_groups:
                    pattern_templates = pattern_groups[pattern_group]
                    for pattern_template in pattern_templates:
                        template_name = pattern_template.origin.template_name
                        break
                    break
                break

        context = self.get_context_data()
        context['templates'] = templates
        context['template_name'] = template_name
        context['pattern_listing'] = render_pattern_listing(template_name)

        return self.render_to_response(context)


class RenderPatternView(TemplateView):
    http_method_names = ('get',)
    template_name = get_pattern_base_template_name()

    def get(self, request, template_name=None):
        try:
            rendered_pattern = render_pattern(request, template_name)
        except TemplateIsNotPattern:
            return HttpResponseBadRequest()

        # Do not render page patterns as part of the base template
        # because it should already extend base template
        if is_pattern_type(template_name, 'pages'):
            return HttpResponse(rendered_pattern)

        context = self.get_context_data()
        context['pattern_library_rendered_pattern'] = rendered_pattern

        return self.render_to_response(context)
