from collections import defaultdict
from operator import attrgetter
from typing import Callable

from django.core.exceptions import ImproperlyConfigured

from .cm_utils import accepts_kwarg, get_app_submodules

GENERIC_CM_KEY = "__generic__"
ORDER_ATTR_NAME = "__cm_order"

__all__ = [
    "ContextModifierRegistry",
    "register_context_modifier"
]


class ContextModifierRegistry(defaultdict):
    def __init__(self):
        super().__init__(list)
        self.searched_for_modifiers = False

    def search_for_modifiers(self) -> None:
        if not self.searched_for_modifiers:
            list(get_app_submodules('pattern_contexts'))
            self.searched_for_modifiers = True

    def register(self, func: Callable, template: str = None, order: int = 0) -> None:
        """
        Adds a context modifier to the registry.
        """
        if not callable(func):
            raise ImproperlyConfigured(
                f"Context modifiers must be callables. {func} is a {type(func).__name__}."
            )
        if not accepts_kwarg(func, "context"):
            raise ImproperlyConfigured(
                f"Context modifiers must accept a 'context' keyword argument. {func} does not."
            )
        if not accepts_kwarg(func, "request"):
            raise ImproperlyConfigured(
                f"Context modifiers must accept a 'request' keyword argument. {func} does not."
            )

        key = template or GENERIC_CM_KEY
        if func not in self[key]:
            setattr(func, ORDER_ATTR_NAME, order)
            self[key].append(func)
            self[key].sort(key=attrgetter(ORDER_ATTR_NAME))

        return func

    def register_decorator(self, func: Callable = None, **kwargs):
        if func is None:
            return lambda func: self.register(func, **kwargs)
        return self.register(func, **kwargs)

    def get_for_template(self, template: str):
        self.search_for_modifiers()
        modifiers = self[GENERIC_CM_KEY] + self[template]
        return sorted(modifiers, key=attrgetter(ORDER_ATTR_NAME))


registry = ContextModifierRegistry()
register_context_modifier = registry.register_decorator
