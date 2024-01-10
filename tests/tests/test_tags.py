from unittest.mock import patch

from django.shortcuts import render
from django.test import RequestFactory, SimpleTestCase

from pattern_library import get_pattern_context_var_name

from .utils import reverse


class TagsTestCase(SimpleTestCase):
    def test_falsey_raw_values_for_tag_output(self):
        response = self.client.get(
            reverse(
                "pattern_library:render_pattern",
                kwargs={
                    "pattern_template_name": "patterns/atoms/tags_test_atom/tags_test_atom.html"
                },
            )
        )
        self.assertContains(response, "SANDWICH")
        self.assertContains(response, "SANDNoneWICH")
        self.assertContains(response, "SAND0WICH")

    def test_default_html_override(self):
        response = self.client.get(
            reverse(
                "pattern_library:render_pattern",
                kwargs={
                    "pattern_template_name": "patterns/atoms/tags_test_atom/tags_test_atom.html"
                },
            )
        )

        self.assertContains(response, "POTAexampleTO")
        self.assertContains(response, "POTAanother_exampleTO")
        self.assertContains(response, "POTAhttps://potato.comTO")

    def test_falsey_default_html_overide(self):
        response = self.client.get(
            reverse(
                "pattern_library:render_pattern",
                kwargs={
                    "pattern_template_name": "patterns/atoms/tags_test_atom/tags_test_atom.html"
                },
            )
        )
        self.assertContains(response, "POTATO1")
        self.assertContains(response, "POTANoneTO2")
        self.assertContains(response, "POTA0TO3")


class TagsTestFailCase(SimpleTestCase):
    def test_bad_default_html_warning(self):
        """
        Test that the library raises a warning when passing a non-string `default_html` argument to `override_tag`
        in Django < 4.0
        """
        with patch("django.VERSION", (3, 2, 0, "final", 0)):
            with self.assertWarns(Warning) as cm:
                template_name = (
                    "patterns/atoms/tags_test_atom/invalid_tags_test_atom.html.fail"
                )
                request = RequestFactory().get("/")

                # Rendering the template with a non-string `default_html` argument will cause Django >= 4 to raise
                # a `TypeError`, which we need to catch and ignore in order to check that the warning is raised
                try:
                    render(
                        request,
                        template_name,
                        context={get_pattern_context_var_name(): True},
                    )
                except TypeError:
                    pass

            self.assertIn(
                "default_html argument to override_tag should be a string to ensure compatibility with Django",
                str(cm.warnings[0]),
            )

    def test_bad_default_html_error(self):
        """
        Test that the library raises a TypeError when passing a non-string `default_html` argument to `override_tag`
        in Django >= 4.0
        """
        with patch("django.VERSION", (4, 2, 0, "final", 0)):
            with self.assertRaises(TypeError) as cm:
                template_name = (
                    "patterns/atoms/tags_test_atom/invalid_tags_test_atom.html.fail"
                )
                request = RequestFactory().get("/")
                render(
                    request,
                    template_name,
                    context={get_pattern_context_var_name(): True},
                )
            self.assertIn(
                "default_html argument to override_tag must be a string",
                str(cm.exception),
            )
