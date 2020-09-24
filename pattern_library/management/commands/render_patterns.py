from pathlib import Path

from django.core.management.base import BaseCommand
from django.test.client import RequestFactory

from pattern_library.utils import (
    get_pattern_templates, render_pattern
)


class Command(BaseCommand):
    help = "Renders all patterns."

    def handle(self, **options):
        templates = get_pattern_templates()
        factory = RequestFactory()
        request = factory.get('/')
        parent_dir = Path.cwd().joinpath('dpl-static')
        parent_dir.mkdir(exist_ok=True)
        self.render_group(request, parent_dir, templates)

    def render_group(self, request, parent_dir: Path, pattern_templates):
        for template in pattern_templates['templates_stored']:
            print(template.origin.template_name)
            print('-------------------')
            render_path = parent_dir.joinpath(template.pattern_name)
            render_path.write_text(render_pattern(request, template.origin.template_name))

        if not pattern_templates['template_groups']:
            return

        for pattern_type_group, pattern_templates in pattern_templates['template_groups'].items():
            print(pattern_type_group)
            group_parent = parent_dir.joinpath(pattern_type_group)
            group_parent.mkdir(exist_ok=True)
            self.render_group(request, group_parent, pattern_templates)
