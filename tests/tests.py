from django.test import SimpleTestCase

from django.core.urlresolvers import reverse


class TestTestCase(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse('pattern_library:index'))
        self.assertEqual(response.status_code, 200)

    # TODO:
    # - add templates and YAML files for tests in this app
    # - test listing views
    # - test context inheritance rules (formalise these first)
    # - test tag overriding
