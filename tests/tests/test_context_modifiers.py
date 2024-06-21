from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.test import SimpleTestCase

from pattern_library import register_context_modifier
from pattern_library.context_modifiers import registry
from pattern_library.utils import render_pattern


def accepts_context_only(context):
    pass


def accepts_request_only(request):
    pass


def modifier_1(context, request):
    context["foo"] = "foo"


def modifier_2(context, request):
    context["foo"] = "bar"


def modifier_3(context, request):
    context["beep"] = "boop"


atom_template = "patterns/atoms/test_atom/test_atom.html"


class ContextModifierTestCase(SimpleTestCase):
    maxDiff = None

    def setUp(self):
        registry.clear()

    def tearDown(self):
        registry.clear()

    def test_validation(self):
        with self.assertRaisesRegex(ImproperlyConfigured, "must be callables"):
            registry.register(0, template=atom_template)
        with self.assertRaisesRegex(
            ImproperlyConfigured, "must accept a 'request' keyword argument"
        ):
            registry.register(accepts_context_only, template=atom_template)
        with self.assertRaisesRegex(
            ImproperlyConfigured, "must accept a 'context' keyword argument"
        ):
            registry.register(accepts_request_only, template=atom_template)

    def test_registered_without_ordering(self):
        registry.register(modifier_1, template=atom_template)
        registry.register(modifier_2, template=atom_template)
        registry.register(modifier_3, template=atom_template)

        result = registry.get_for_template(atom_template)
        self.assertEqual(
            result,
            [
                modifier_1,
                modifier_2,
                modifier_3,
            ],
        )

    def test_registered_with_ordering(self):
        registry.register(modifier_1, template=atom_template, order=10)
        registry.register(modifier_2, template=atom_template, order=5)
        registry.register(modifier_3, template=atom_template, order=0)

        result = registry.get_for_template(atom_template)
        self.assertEqual(
            result,
            [
                modifier_3,
                modifier_2,
                modifier_1,
            ],
        )

    def test_registered_via_decorator(self):
        @register_context_modifier(order=100)
        def func_a(context, request):
            pass

        @register_context_modifier(order=50)
        def func_b(context, request):
            pass

        @register_context_modifier(template=atom_template)
        def func_c(context, request):
            pass

        @register_context_modifier(template="different_template.html", order=1)
        def func_x(context, request):  # NOQA
            pass

        result = registry.get_for_template(atom_template)
        self.assertEqual(
            result,
            [
                func_c,
                func_b,
                func_a,
            ],
        )

    @mock.patch("pattern_library.utils.render_to_string")
    def test_applied_by_render_pattern(self, render_to_string):
        request = HttpRequest()
        registry.register(modifier_1)
        registry.register(modifier_2, template=atom_template)
        registry.register(modifier_3, template=atom_template)

        render_pattern(request, atom_template)
        render_to_string.assert_called_with(
            atom_template,
            request=request,
            context={
                "atom_var": "atom_var value from test_atom.yaml",
                "is_pattern_library": True,
                "__pattern_library_tag_overrides": {},
                "foo": "bar",
                "beep": "boop",
            },
        )
