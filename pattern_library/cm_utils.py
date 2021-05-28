
import inspect
from importlib import import_module
from typing import Callable

from django.apps import apps
from django.utils.module_loading import module_has_submodule


def get_app_modules():
    """
    Generator function that yields a module object for each installed app
    yields tuples of (app_name, module)
    """
    for app in apps.get_app_configs():
        yield app.name, app.module


def get_app_submodules(submodule_name):
    """
    Searches each app module for the specified submodule
    yields tuples of (app_name, module)
    """
    for name, module in get_app_modules():
        if module_has_submodule(module, submodule_name):
            yield name, import_module('%s.%s' % (name, submodule_name))


def accepts_kwarg(func: Callable, kwarg: str) -> bool:
    """
    Returns a boolean indicating whether the callable  ``func`` has
    a signature that accepts the keyword argument ``kwarg``.
    """
    signature = inspect.signature(func)
    try:
        signature.bind_partial(**{kwarg: None})
        return True
    except TypeError:
        return False
