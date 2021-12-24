import os

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from pattern_library.utils import (
    get_template_ancestors, get_template_dirs, get_pattern_config_str,
)


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


class TestGetPatternConfigStr(SimpleTestCase):
    def test_not_existing_template(self):
        result = get_pattern_config_str("doesnotexist")

        self.assertEqual(result, "")

    def test_atom_yaml(self):
        result = get_pattern_config_str("patterns/atoms/test_atom/test_atom.html")

        self.assertNotEqual(result, "")
        self.assertIn("atom_var value from test_atom.yaml", result)

    def test_atom_yml(self):
        result = get_pattern_config_str("patterns/atoms/test_atom_yml/test_atom_yml.html")

        self.assertNotEqual(result, "")
        self.assertIn("atom_var value from test_atom.yml", result)
