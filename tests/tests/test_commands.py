import io

import tempfile
from pathlib import Path
import shutil

from django.test import SimpleTestCase
from django.core.management import call_command


class RenderPatternsTests(SimpleTestCase):
    """Tests of the render_pattern command’s output, based on the test project’s templates"""

    def test_displays_patterns(self):
        stdout = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout)
        stdout = stdout.getvalue()
        self.assertIn("""patterns/atoms/tags_test_atom/tags_test_atom.html
patterns/atoms/test_atom/test_atom.html
""", stdout)

    def test_verbose_output(self):
        stdout = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, verbosity=2)
        stdout = stdout.getvalue()
        self.assertIn("""Target directory: dpl-rendered-patterns
Group: atoms
Group: tags_test_atom
Pattern: tags_test_atom.html
patterns/atoms/tags_test_atom/tags_test_atom.html


SANDWICH
SANDNoneWICH
SAND0WICH
""", stdout)

    def test_quiet_output(self):
        stdout = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, verbosity=0)
        stdout = stdout.getvalue()
        self.assertEqual(stdout, '')

    def test_shows_output_folder(self):
        stdout = io.StringIO()
        temp = tempfile.gettempdir()
        call_command('render_patterns', dry_run=True, stdout=stdout, output=temp, verbosity=2)
        stdout = stdout.getvalue()
        self.assertIn(temp, stdout)


class RenderPatternsFileSystemTests(SimpleTestCase):
    """Tests of the render_pattern command’s file system changes, based on the test project’s templates"""

    def setUp(self):
        self.output = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output)

    def test_uses_output(self):
        stdout = io.StringIO()
        modification_time_before = Path(self.output).stat().st_mtime
        call_command('render_patterns', dry_run=False, stdout=stdout, output=self.output)
        self.assertNotEqual(Path(self.output).stat().st_mtime, modification_time_before)
        stdout = stdout.getvalue()

    def test_uses_subfolders(self):
        stdout = io.StringIO()
        call_command('render_patterns', dry_run=False, stdout=stdout, output=self.output)
        subfolders = Path(self.output).iterdir()
        self.assertIn('atoms', [p.name for p in subfolders])

    def test_outputs_html(self):
        stdout = io.StringIO()
        call_command('render_patterns', dry_run=False, stdout=stdout, output=self.output)
        html_files = Path(self.output).glob('**/*.html')
        self.assertIn('test_atom.html', [p.name for p in html_files])
