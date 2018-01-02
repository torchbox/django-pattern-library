from django.test import SimpleTestCase

from django.core.urlresolvers import reverse


class ViewsTestCase(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse('pattern_library:index'))
        self.assertEqual(response.status_code, 200)


class ContextTestCase(SimpleTestCase):
    def test_context_from_file(self):
        response = self.client.get(reverse(
            'pattern_library:display_pattern',
            kwargs={'template_name': 'patterns/atoms/test_atom/test_atom.html'},
        ))
        self.assertContains(response, 'atom_var value from test_atom.yaml')

    def test_including_context_overrides_included_context(self):
        response = self.client.get(reverse(
            'pattern_library:display_pattern',
            kwargs={'template_name': 'patterns/molecules/test_molecule/test_molecule.html'},
        ))
        self.assertContains(response, 'atom_var value from test_molecule.yaml')
        self.assertContains(response, 'atom_var value from test_molecule.html include tag')
        self.assertNotContains(response, 'atom_var value from test_atom.html')


class TagsTesCase(SimpleTestCase):
    pass
