
import inspect
from typing import Callable


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
