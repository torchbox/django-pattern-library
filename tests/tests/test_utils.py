from django.test import SimpleTestCase

from pattern_library.utils import get_template_ancestors


class TestGetTemplateAncestors(SimpleTestCase):
    def test_page(self):
        self.assertEqual(
            get_template_ancestors('patterns/pages/test_page/test_page.html'),
            [
                'patterns/pages/test_page/test_page.html',
                'patterns/base_page.html',
                'patterns/base.html',
            ],
        )

    def test_fragment(self):
        self.assertEqual(
            get_template_ancestors('patterns/atoms/test_atom/test_atom.html'),
            [
                'patterns/atoms/test_atom/test_atom.html',
            ],
        )

    def test_parent_template_from_variable(self):
        self.assertEqual(
            get_template_ancestors(
                'patterns/atoms/test_extends/extended.html',
                context={'parent_template_name': 'patterns/base.html'},
            ),
            [
                'patterns/atoms/test_extends/extended.html',
                'patterns/base.html',
            ],
        )
