import io
import shutil
import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import SimpleTestCase


class RenderPatternsTests(SimpleTestCase):
    """Tests of the render_pattern command’s output, based on the test project’s templates"""

    def test_displays_patterns(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, stderr=stderr)
        self.assertIn("""patterns/atoms/tags_test_atom/tags_test_atom.html
patterns/atoms/test_atom/test_atom.html
""", stderr.getvalue())

    def test_verbose_output(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, stderr=stderr, verbosity=2)
        self.assertIn("""Target directory: dpl-rendered-patterns. Dry run, not writing files to disk
Group: atoms
Group: icons
Pattern: icon.html
patterns/atoms/icons/icon.html
""", stderr.getvalue())
        self.assertIn("""<svg class="icon icon--close" aria-hidden="true" focusable="false">
    <use xlink:href="#close"></use>
</svg>""", stdout.getvalue())

    def test_quiet_output(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, stderr=stderr, verbosity=0)
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), '')

    def test_shows_output_folder(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        temp = tempfile.gettempdir()
        call_command('render_patterns', dry_run=True, stdout=stdout, stderr=stderr, output=temp, verbosity=2)
        self.assertIn(temp, stderr.getvalue())

    def test_shows_wrap_fragment(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=True, wrap_fragments=True, stdout=stdout, stderr=stderr, verbosity=2)
        self.assertIn('Writing fragment patterns wrapped in base template', stderr.getvalue())
        # Only testing a small subset of the output just to show patterns are wrapped.
        self.assertIn("""<svg class="icon icon--close" aria-hidden="true" focusable="false">
    <use xlink:href="#close"></use>
</svg>

        </main>
        <script src="/static/main.js"></script>
    </body>
</html>""", stdout.getvalue())

    def test_saves_with_template_filename(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=True, stdout=stdout, stderr=stderr, verbosity=2)
        self.assertIn('Pattern: test_molecule.html', stderr.getvalue())


class RenderPatternsFileSystemTests(SimpleTestCase):
    """Tests of the render_pattern command’s file system changes, based on the test project’s templates"""

    def setUp(self):
        self.output = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output)

    def test_uses_output(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        modification_time_before = Path(self.output).stat().st_mtime
        call_command('render_patterns', dry_run=False, stdout=stdout, stderr=stderr, output=self.output)
        self.assertNotEqual(Path(self.output).stat().st_mtime, modification_time_before)

    def test_uses_subfolders(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=False, stdout=stdout, stderr=stderr, output=self.output)
        subfolders = Path(self.output).iterdir()
        self.assertIn('atoms', [p.name for p in subfolders])

    def test_outputs_html(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        call_command('render_patterns', dry_run=False, stdout=stdout, stderr=stderr, output=self.output)
        html_files = Path(self.output).glob('**/*.html')
        self.assertIn('test_atom.html', [p.name for p in html_files])
