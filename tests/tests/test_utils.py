import os

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from pattern_library.utils import get_template_ancestors, get_template_dirs


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


class TestGetTemplateDirs(SimpleTestCase):
    def get_relative_template_dirs(self):
        """Make paths relative with a predefined root so we can use them in assertions."""
        base = os.path.dirname(settings.BASE_DIR)
        dirs = get_template_dirs()
        return ['/'.join(str(d).replace(base, 'dpl').split('/')[-4:-1]) for d in dirs]

    @override_settings(TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        },
    ])
    def test_get_template_dirs_app_dirs(self):
        self.assertListEqual(self.get_relative_template_dirs(), [
            'django/contrib/auth',
            'dpl/pattern_library',
            'dpl/tests',
        ])

    @override_settings(TEMPLATES=[
        {
            'NAME': 'one',
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(settings.BASE_DIR, "test_one", "templates")],
            'APP_DIRS': True,
        },
        {
            'NAME': 'two',
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(settings.BASE_DIR, "test_two", "templates")],
        },
    ])
    def test_get_template_dirs_list_dirs(self):
        self.assertListEqual(self.get_relative_template_dirs(), [
            'dpl/tests/test_one',
            'dpl/tests/test_two',
            'django/contrib/auth',
            'dpl/pattern_library',
            'dpl/tests',
        ])
