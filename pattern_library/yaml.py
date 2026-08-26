from functools import partial, wraps

from yaml.loader import FullLoader
from yaml.nodes import MappingNode, SequenceNode

# Define our own yaml loader so we can register constructors on it without
# polluting the original loader from the library.
class PatternLibraryLoader(FullLoader):
    pass


def _yaml_tag_constructor(fn):
    """
    Convert the given function into a PyYAML-compatible constructor that
    correctly parses it args/kwargs.
    """
    @wraps(fn)
    def constructor(loader, node):
        args, kwargs = (), {}
        if isinstance(node, SequenceNode):
            args = loader.construct_sequence(node, deep=True)
        elif isinstance(node, MappingNode):
            kwargs = loader.construct_mapping(node, deep=True)
        else:
            pass  # No arguments given
        return fn(*args, **kwargs)

    return constructor


def register_yaml_tag(fn=None, name=None):
    """
    Register the given function as a custom (local) YAML tag under the given name.
    """

    # This set of if statements is fairly complex so we can support a variety
    # of ways to call the decorator:

    # @register_yaml_tag()
    if fn is None and name is None:  # @register_yaml_tag()
        return partial(register_yaml_tag, name=None)

    # @register_yaml_tag(name="asdf")
    elif fn is None and name is not None:
        return partial(register_yaml_tag, name=name)

    # @register_yaml_tag("asdf")
    elif isinstance(fn, str) and name is None:  
        return partial(register_yaml_tag, name=fn)

    # @register_yaml_tag
    elif fn is not None and name is None:
        return register_yaml_tag(fn, name=fn.__name__)

    # At this point, both `fn` and `name` are defined
    PatternLibraryLoader.add_constructor(f"!{name}", _yaml_tag_constructor(fn))
    return fn


def unregister_yaml_tag(name):
    """
    Unregister the custom tag with the given name.
    """
    # PyYAML doesn't provide an inverse operation for add_constructor(), so
    # we need to do it manually.
    del PatternLibraryLoader.yaml_constructors[f"!{name}"]
