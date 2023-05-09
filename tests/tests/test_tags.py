from django.test import SimpleTestCase
from unittest.mock import patch

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

    def test_bad_default_html_warning(self):
        with patch("django.VERSION", (3, 2, 0, "final", 0)):
            with self.assertWarns(Warning) as cm:
                response = self.client.get(
                    reverse(
                        "pattern_library:render_pattern",
                        kwargs={
                            "pattern_template_name": "patterns/atoms/tags_test_atom/invalid_tags_test_atom.html",
                        },
                    ),
                )
                self.assertContains(response, "MARMALADE01")
                self.assertContains(response, "MARMANoneLADE02")
                self.assertIn(
                    "default_html argument to override_tag should be a string to ensure compatibility with Django",
                    str(cm.warnings[0]),
                )

    def test_bad_default_html_error(self):
        with patch("django.VERSION", (4, 2, 0, "final", 0)):
            with self.assertRaises(TypeError) as cm:
                self.client.get(
                    reverse(
                        "pattern_library:render_pattern",
                        kwargs={"pattern_template_name": "patterns/atoms/tags_test_atom/invalid_tags_test_atom.html"},
                    ),
                )
            self.assertIn("default_html argument to override_tag must be a string", str(cm.exception))
