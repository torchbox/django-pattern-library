from django.core.urlresolvers import reverse
from django.test import SimpleTestCase


class ViewsTestCase(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse('pattern_library:index'))
        self.assertEqual(response.status_code, 200)
