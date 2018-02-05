from django.core.urlresolvers import reverse
from django.test import SimpleTestCase


class TagsTesCase(SimpleTestCase):
    def test_falsey_raw_values_for_tag_output(self):
        response = self.client.get(reverse(
            'pattern_library:display_pattern',
            kwargs={'template_name': 'patterns/atoms/tags_test_atom/tags_test_atom.html'},
        ))
        self.assertContains(response, "SANDWICH")
        self.assertContains(response, "SANDNoneWICH")
        self.assertContains(response, "SAND0WICH")
