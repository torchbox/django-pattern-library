from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView

from pattern_library import get_pattern_types, get_pattern_base_template_name
from pattern_library.exceptions import TemplateIsNotPattern
from pattern_library.utils import get_pattern_templates, render_pattern, is_pattern_type


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get(self, request, *args, **kwargs):
        available_pattern_types = get_pattern_types()
        pattern_types_to_display = available_pattern_types

        # Render only specific pattern types,
        # if `pattern_type` is supplied
        if 'pattern_type' in kwargs:
            pattern_type = kwargs['pattern_type'].lower()
            if pattern_type not in available_pattern_types:
                return HttpResponseBadRequest()
            pattern_types_to_display = [pattern_type]

        # Get all pattern templates for a specific types
        templates = get_pattern_templates(pattern_types_to_display)

        context = self.get_context_data(**kwargs)
        context['templates'] = templates
        return self.render_to_response(context)


class PatternView(TemplateView):
    http_method_names = ('get', )
    template_name = get_pattern_base_template_name()

    def get(self, request, *args, **kwargs):
        pattern_template_name = kwargs['template_name']

        try:
            rendered_pattern = render_pattern(request, pattern_template_name)
        except TemplateIsNotPattern:
            return HttpResponseBadRequest()

        # Dp not render page patterns as part of the base template
        # because it should already extend base template
        if is_pattern_type(pattern_template_name, 'pages'):
            return HttpResponse(rendered_pattern)

        context = self.get_context_data(**kwargs)
        context['pattern_library_rendered_pattern'] = rendered_pattern
        return self.render_to_response(context)
