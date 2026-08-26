from unittest import mock

import yaml
from django.test import SimpleTestCase
from yaml.constructor import ConstructorError

from pattern_library.utils import get_pattern_context
from pattern_library.yaml import (
    register_yaml_tag,
    unregister_yaml_tag,
)


class PatternLibraryLoaderTestCase(SimpleTestCase):
    def tearDown(self):
        super().tearDown()
        # Make sure any custom tag is unregistered after every test
        try:
            unregister_yaml_tag("customtag")
        except KeyError:
            pass

    def _get_context(self, yaml_str):
        # Use mock.patch to avoid having to create actual files on disk
        with mock.patch("pattern_library.utils.get_pattern_config_str", return_value=yaml_str):
            return get_pattern_context("mocked.html")

    def assertContextEqual(self, yaml_str, expected, msg=None):
        """
        Check that the given yaml string can be loaded and results in the given context.
        """
        context = self._get_context(yaml_str)
        self.assertEqual(context, expected, msg=msg)

    def test_unknown_tag_throws_error(self):
        self.assertRaises(
            ConstructorError,
            self._get_context,
            "context:\n  test: !customtag"
        )

    def test_custom_tag_can_be_registered(self):
        register_yaml_tag(lambda: 42, "customtag")
        self.assertContextEqual(
            "context:\n  test: !customtag",
            {"test": 42},
        )

    def test_custom_tag_can_be_unregistered(self):
        register_yaml_tag(lambda: 42, "customtag")
        unregister_yaml_tag("customtag")
        self.assertRaises(
            ConstructorError,
            self._get_context,
            "context:\n  test: !customtag"
        )

    def test_custom_tag_registering_doesnt_pollute_parent_loader(self):
        register_yaml_tag(lambda: 42, "customtag")
        self.assertRaises(
            ConstructorError,
            yaml.load,
            "context:\n  test: !customtag",
            Loader=yaml.FullLoader,
        )

    def test_registering_plain_decorator(self):
        @register_yaml_tag
        def customtag():
            return 42

        self.assertContextEqual(
            "context:\n  test: !customtag",
            {"test": 42},
        )

    def test_registering_plain_decorator_called(self):
        @register_yaml_tag()
        def customtag():
            return 42

        self.assertContextEqual(
            "context:\n  test: !customtag",
            {"test": 42},
        )

    def test_registering_decorator_specify_name(self):
        @register_yaml_tag("customtag")
        def function_with_different_name():
            return 42

        self.assertContextEqual(
            "context:\n  test: !customtag",
            {"test": 42},
        )

    def test_registering_decorator_specify_name_kwarg(self):
        @register_yaml_tag(name="customtag")
        def function_with_different_name():
            return 42

        self.assertContextEqual(
            "context:\n  test: !customtag",
            {"test": 42},
        )

    def test_custom_tag_with_args(self):
        register_yaml_tag(lambda *a: sum(a), "customtag")

        yaml_str = """
context:
  test: !customtag
    - 1
    - 2
    - 3
        """.strip()

        self.assertContextEqual(yaml_str, {"test": 6})

    def test_custom_tag_with_kwargs(self):
        register_yaml_tag(lambda **kw: {k.upper(): v for k, v in kw.items()}, "customtag")

        yaml_str = """
context:
  test: !customtag
    key1: 1
    key2: 2
        """.strip()

        self.assertContextEqual(yaml_str, {"test": {"KEY1": 1, "KEY2": 2}})
