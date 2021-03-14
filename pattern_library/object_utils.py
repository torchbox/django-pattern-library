import functools
import inspect
from importlib import import_module
from typing import Any, Callable, Dict, Type

from django.conf import settings
from django.http.request import HttpRequest


@functools.lru_cache(maxsize=None)
def import_from_path(path: str) -> Type:
    module_path, object_name = path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, object_name)


@functools.lru_cache(maxsize=None)
def accepts_kwarg(func: Callable, kwarg: str) -> bool:
    """
    Returns a boolean indicating whether the callable  ``func`` has a
    signature that accepts the keyword argument `kwarg`
    """
    signature = inspect.signature(func)
    try:
        signature.bind_partial(**{kwarg: None})
        return True
    except TypeError:
        return False


def get_custom_factories() -> Dict:
    return getattr(settings, "PATTERN_LIBRARY_CUSTOM_FACTORIES", {})


def get_common_object_definitions() -> Dict:
    return getattr(settings, "PATTERN_LIBRARY_COMMON_OBJECTS", {})


def simple_object_factory(
    klass: Type, definition: Dict[str, Any], request: HttpRequest, template_name: str
) -> Any:
    """
    Creates an instance of type ``klass`` using the remaining key/value pairs
    from the ``definition`` and the current ``request``. Any key/value pairs
    NOT accepted by the classes ``__init__`` method are set as attributes on
    the object after initialisation.
    """
    init_kwargs = {}
    attributes = {}
    for key, value in definition.items():
        if accepts_kwarg(klass.__init__, key):
            init_kwargs[key] = value
        else:
            attributes[key] = value
    if accepts_kwarg(klass.__init__, "request"):
        init_kwargs["request"] = request
    obj = klass(**init_kwargs)
    for attr, value in attributes.items():
        setattr(obj, attr, value)
    return klass(**definition)


def make_object(
    definition: Dict[str, Any],
    context: Dict[str, Any],
    request: HttpRequest,
    template_name: str,
) -> Any:
    """
    Converts an object defintion to an instance of the relevant class,
    by importing the class, finding a suitable 'factory' function and
    passing everything on to it.
    """
    classname = definition.pop("klass")
    custom_factories = get_custom_factories()
    if classname in custom_factories:
        factory = import_from_path(custom_factories[classname])
    else:
        factory = simple_object_factory
    return factory(
        import_from_path(classname),
        definition=definition,
        context=context,
        request=request,
        template_name=template_name,
    )


def get_common_objects(
    context: Dict[str, Any], request: HttpRequest, template_name: str
) -> Dict[str, Any]:
    """
    Returns a dictionary of objects to be added to all pattern template
    contexts, as defined by the ``PATTERN_LIBRARY_COMMON_OBJECTS`` setting.

    All arguments passed to this method are for 'passing through' to object
    factories only. ``inject_python_objects()`` is responsible for working
    the return value into the template context.
    """
    objects = {}
    for key, value in get_common_object_definitions().items():
        definition = {}
        if isinstance(value, str):
            definition["klass"] = value
        if isinstance(value, dict):
            definition.update(value)
        if definition:
            objects[key] = make_object(definition, context, request, template_name)
    return objects


def replace_object_definitions(
    search_dict: Dict[str, Any],
    context: Dict[str, Any],
    request: HttpRequest,
    template_name: str,
) -> None:
    """
    Recursively evaluates ``search_dict``, looking for dictionaries that
    look like object definitions, and replacing those defintions with
    instances of the relevant class.
    """
    for key, value in dict(search_dict).items():
        if isinstance(value, dict):
            replace_object_definitions(value, context, request, template_name)
            if "klass" in value:
                search_dict[key] = make_object(value, context, request, template_name)


def inject_python_objects(
    context: Dict[str, Any],
    request: HttpRequest,
    template_name: str,
) -> None:
    context.update(get_common_objects(context, request, template_name))
    replace_object_definitions(context, context, request, template_name)
