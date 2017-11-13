import os

from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView

from pattern_library import get_base_lookup_dir


class IndexView(TemplateView):
    template_name = 'pattern_library/index.html'
    pattern_types = ['atoms', 'molecules', 'organisms', 'templates', 'organisms']
    pattern_template_suffix = '.html'

    def get_context_data(self, **kwargs):
        templates = self.get_pattern_templates()

        context = super().get_context_data()
        context['templates'] = templates
        return context

    def get_pattern_templates(self):
        templates = {}
        base_lookup_dir = get_base_lookup_dir()
        lookup_dir = os.path.join(base_lookup_dir, 'patterns')

        for pattern_type in self.pattern_types:
            for root, dirs, files in os.walk(os.path.join(lookup_dir, pattern_type)):
                pattern_subtype = os.path.relpath(root, lookup_dir)

                pattern_types_templates = templates.get(pattern_type, {})

                for current_file in files:
                    path = os.path.join(root, current_file)
                    path = os.path.relpath(path, base_lookup_dir)

                    # Include only templates
                    pattern_types_templates[pattern_subtype] = get_template(path)

                templates[pattern_type] = pattern_types_templates

        return templates
