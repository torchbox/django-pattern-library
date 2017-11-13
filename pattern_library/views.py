from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import TemplateView, View

from pattern_library.exceptions import TemplateIsNotPattern
from pattern_library.utils import get_pattern_templates, render_pattern


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get_context_data(self, **kwargs):
        templates = get_pattern_templates()

        context = super().get_context_data()
        context['templates'] = templates
        return context


class PatternView(View):
    def get(self, request, template_name):
        try:
            content = render_pattern(request, template_name)
        except TemplateIsNotPattern:
            return HttpResponseBadRequest()

        return HttpResponse(content)
