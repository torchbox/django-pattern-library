from django.test import SimpleTestCase

from bs4 import BeautifulSoup

from .utils import reverse


class ViewsTestCase(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse('pattern_library:index'))
        self.assertEqual(response.status_code, 200)

    def test_pretty_names_from_context(self):
        test_molecule_display_url = reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule.html'},
        )
        test_molecule_render_url = reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule.html'},
        )

        response = self.client.get(test_molecule_display_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content)

        display_link = soup.select_one(f'a[href="{test_molecule_display_url}"]')
        render_link = soup.select_one(f'a[href="{test_molecule_render_url}"]')

        self.assertEqual(display_link.text.strip(), "Pretty name for test molecule")
        self.assertEqual(render_link.text.strip(), "Pretty name for test molecule")

    def test_pretty_names_from_filename(self):
        test_molecule_display_url = reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule_no_context.html'},
        )
        test_molecule_render_url = reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule_no_context.html'},
        )

        response = self.client.get(test_molecule_display_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content)

        display_link = soup.select_one(f'a[href="{test_molecule_display_url}"]')
        render_link = soup.select_one(f'a[href="{test_molecule_render_url}"]')

        self.assertEqual(display_link.text.strip(), "test_molecule_no_context.html")
        self.assertEqual(render_link.text.strip(), "test_molecule_no_context.html")
