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

        soup = BeautifulSoup(response.content, features="html.parser")

        display_link = soup.select_one(f'a[href="{test_molecule_display_url}"]')
        render_link = soup.select_one(f'a[href="{test_molecule_render_url}"]')

        self.assertEqual(display_link.text.strip(), "Pretty name for test molecule")
        self.assertEqual(render_link.text.strip(), "Pretty name for test molecule")

    def test_pretty_names_from_filename(self):
        pattern_path = 'patterns/molecules/test_molecule/test_molecule_no_context.html'
        test_molecule_display_url = reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': pattern_path},
        )
        test_molecule_render_url = reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': pattern_path},
        )

        response = self.client.get(test_molecule_display_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, features="html.parser")

        display_link = soup.select_one(f'.list__item>a[href="{test_molecule_display_url}"]')
        render_link = soup.select_one(f'a[href="{test_molecule_render_url}"]')

        self.assertEqual(display_link.text.strip(), "test_molecule_no_context.html")
        self.assertEqual(render_link.text.strip(), pattern_path)

    def test_includes(self):
        pattern_path = 'patterns/atoms/test_includes/test_includes.html'
        display_url = reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': pattern_path},
        )
        render_url = reverse(
            'pattern_library:render_pattern',
            kwargs={'pattern_template_name': pattern_path},
        )

        display_response = self.client.get(display_url)
        self.assertEqual(display_response.status_code, 200)

        render_response = self.client.get(render_url)
        self.assertEqual(render_response.status_code, 200)
        self.assertContains(render_response, 'SHOWME')
        self.assertNotContains(render_response, 'HIDEME')
