from django.test import SimpleTestCase

from .utils import reverse


class TagsTesCase(SimpleTestCase):
    def test_falsey_raw_values_for_tag_output(self):
        response = self.client.get(reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': 'patterns/atoms/tags_test_atom/tags_test_atom.html'},
        ))
        self.assertContains(response, "SANDWICH")
        self.assertContains(response, "SANDNoneWICH")
        self.assertContains(response, "SAND0WICH")
    
    def test_default_override(self):
        response = self.client.get(reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': 'patterns/atoms/tags_test_atom/tags_test_atom.html'},
        ))

        self.assertContains(response, "POTAexampleTO")
        self.assertContains(response, "POTAanother_exampleTO")
        self.assertContains(response, "POTAhttps://potato.comTO")

