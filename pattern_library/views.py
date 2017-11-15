from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView, View

from pattern_library import get_pattern_types
from pattern_library.exceptions import TemplateIsNotPattern
from pattern_library.utils import get_pattern_templates, render_pattern


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get(self, request, *args, **kwargs):
        available_pattern_types = get_pattern_types()
        pattern_types = available_pattern_types

        # Render only specific pattern types,
        # if `pattern_type` is supplied
        if 'pattern_type' in kwargs:
            pattern_types = kwargs['pattern_type'].lower()
            if pattern_types not in available_pattern_types:
                return HttpResponseBadRequest()
            pattern_types = [pattern_types]

        # Get all pattern templates for a specific types
        templates = get_pattern_templates(pattern_types)

        context = self.get_context_data(**kwargs)
        context['templates'] = templates
        return self.render_to_response(context)


class PatternView(View):
    def get(self, request, template_name):
        # TODO: Decide if we need to render associated data recursively
        # TODO: Add a base template

        try:
            content = render_pattern(request, template_name)
        except TemplateIsNotPattern:
            return HttpResponseBadRequest()

        return HttpResponse(content)
