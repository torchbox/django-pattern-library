from django.conf import settings
from django.test import SimpleTestCase, override_settings

from bs4 import BeautifulSoup

from .utils import reverse


class SectionsTestCase(SimpleTestCase):
    def get_sections(self):
        response = self.client.get(reverse('pattern_library:index'))
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, features='html.parser')
        sidebar_nav = soup.select_one('#sidebar-nav')
        sections = [h.text.strip() for h in sidebar_nav.find_all('h2')]

        return sections

    def test_just_atoms(self):
        pl_settings = settings.PATTERN_LIBRARY

        with override_settings(PATTERN_LIBRARY={
            'TEMPLATE_DIR': pl_settings['TEMPLATE_DIR'],
            'SECTIONS': [
                ('atoms', ['patterns/atoms']),
            ]
        }):
            # Check the section list in the sidebar only contains the Atoms sections
            sections = self.get_sections()
            self.assertListEqual(sections, ['Atoms'])

            # Check a pattern from Atoms can be rendered
            test_atom_render_url = reverse(
                'pattern_library:render_pattern',
                kwargs={'pattern_template_name': 'patterns/atoms/test_atom/test_atom.html'},
            )

            response = self.client.get(test_atom_render_url)
            self.assertEqual(response.status_code, 200)

            # Check a pattern from Molecules cannot be rendered
            test_molecule_render_url = reverse(
                'pattern_library:render_pattern',
                kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule.html'},
            )

            response = self.client.get(test_molecule_render_url)
            self.assertEqual(response.status_code, 404)
