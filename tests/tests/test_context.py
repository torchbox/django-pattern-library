from django.test import SimpleTestCase
from django.utils.safestring import SafeText

from .utils import reverse


class ContextTestCase(SimpleTestCase):
    def test_context_from_file(self):
        response = self.client.get(reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': 'patterns/atoms/test_atom/test_atom.html'},
        ))
        self.assertContains(response, 'atom_var value from test_atom.yaml')

    def test_including_context_overrides_included_context(self):
        response = self.client.get(reverse(
            'pattern_library:display_pattern',
            kwargs={'pattern_template_name': 'patterns/molecules/test_molecule/test_molecule.html'},
        ))
        self.assertContains(response, 'atom_var value from test_molecule.yaml')
        self.assertContains(response, 'atom_var value from test_molecule.html include tag')
        self.assertNotContains(response, 'atom_var value from test_atom.html')

    def test_marking_strings_safe_in_context(self):
        from pattern_library.utils import mark_context_strings_safe

        context = {
            'str': 'str',
            'list': ['str', 'str'],
            'dict': {
                'a': 'str',
                'b': 'str',
                'c': 'str',
            },
            'complex': {
                'nested_list': [['0_0', '0_1'], ['1_0', '1_1']],
                'nested_dict': {
                    'a': 'b',
                    'c': 'd',
                },
            },
            1: 2,  # Just here to check they don't cause errors
        }

        mark_context_strings_safe(context)

        self.assertTrue(isinstance(context['str'], SafeText))

        for value in context['list']:
            self.assertTrue(isinstance(value, SafeText))

        for key, value in context['dict'].items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, SafeText))

        complex_value = context['complex']
        for key in complex_value.keys():
            self.assertTrue(isinstance(key, str))

        nested_list = complex_value['nested_list']
        for sub_list in nested_list:
            for value in sub_list:
                self.assertTrue(isinstance(value, SafeText))

        nested_dict = complex_value['nested_dict']
        for key, value in nested_dict.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, SafeText))
