from pathlib import Path

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.test.client import RequestFactory

from pattern_library import (
    get_base_template_names, get_pattern_base_template_name
)
from pattern_library.utils import (
    get_pattern_context, get_pattern_templates, get_template_ancestors,
    render_pattern
)


class Command(BaseCommand):
    help = "Renders all django-pattern-library patterns to HTML files, in a directory structure."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--output',
            '-o',
            action='store',
            dest='output_dir',
            default='dpl-rendered-patterns',
            help='Directory where to render your patterns',
            type=str,
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Render the patterns without writing them to disk.",
        )
        parser.add_argument(
            '--wrap-fragments',
            action='store_true',
            help="Render fragment patterns wrapped in the base template.",
        )

    def handle(self, **options):
        self.verbosity = options['verbosity']
        self.dry_run = options['dry_run']
        self.wrap_fragments = options['wrap_fragments']
        self.output_dir = options['output_dir']

        templates = get_pattern_templates()

        factory = RequestFactory()
        request = factory.get('/')

        if self.verbosity >= 2:
            if self.dry_run:
                self.stderr.write(f'Target directory: {self.output_dir}. Dry run, not writing files to disk')
            else:
                self.stderr.write(f'Target directory: {self.output_dir}')

            if self.wrap_fragments:
                self.stderr.write('Writing fragment patterns wrapped in base template')

        # Resolve the output dir according to the directory the command is run from.
        parent_dir = Path.cwd().joinpath(self.output_dir)

        if not self.dry_run:
            parent_dir.mkdir(exist_ok=True)

        self.render_group(request, parent_dir, templates)

    def render_group(self, request, parent_dir: Path, pattern_templates):
        for template in pattern_templates['templates_stored']:
            if self.verbosity >= 2:
                self.stderr.write(f'Pattern: {template.pattern_filename}')
            if self.verbosity >= 1:
                self.stderr.write(template.origin.template_name)

            render_path = parent_dir.joinpath(template.pattern_filename)
            rendered_pattern = self.render_pattern(request, template.origin.template_name)

            if self.dry_run:
                if self.verbosity >= 2:
                    self.stdout.write(rendered_pattern)
            else:
                render_path.write_text(rendered_pattern)

        if not pattern_templates['template_groups']:
            return

        for pattern_type_group, pattern_templates in pattern_templates['template_groups'].items():
            if self.verbosity >= 2:
                self.stderr.write(f'Group: {pattern_type_group}')
            group_parent = parent_dir.joinpath(pattern_type_group)
            if not self.dry_run:
                group_parent.mkdir(exist_ok=True)
            self.render_group(request, group_parent, pattern_templates)

    def render_pattern(self, request, pattern_template_name):
        rendered_pattern = render_pattern(request, pattern_template_name)

        # If we don’t wrap fragments in the base template, we can simply render the pattern and return as-is.
        if not self.wrap_fragments:
            return rendered_pattern

        pattern_template_ancestors = get_template_ancestors(
            pattern_template_name,
            context=get_pattern_context(pattern_template_name),
        )
        pattern_is_fragment = set(pattern_template_ancestors).isdisjoint(set(get_base_template_names()))

        if pattern_is_fragment:
            base_template = get_pattern_base_template_name()
            context = get_pattern_context(base_template)
            context['pattern_library_rendered_pattern'] = rendered_pattern
            return render_to_string(base_template, request=request, context=context)
        else:
            return rendered_pattern
