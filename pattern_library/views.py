from django.views.generic.base import TemplateView

from pattern_library.utils import get_pattern_templates


class IndexView(TemplateView):
    http_method_names = ('get', )
    template_name = 'pattern_library/index.html'

    def get_context_data(self, **kwargs):
        templates = get_pattern_templates()

        context = super().get_context_data()
        context['templates'] = templates
        return context
