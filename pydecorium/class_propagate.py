from .decorator import Decorator
from typing import Optional, List
import types

def class_propagate(decorator: Decorator, methods: Optional[List[str]] = None):  
    """
    Applies a given decorator to specific methods of a class. 

    .. note::

        This decorator is intended to be used on classes.
        Only methods that are regular functions (of type `types.FunctionType`) will be targeted.
        Does not apply the decorator to special methods (e.g., `__init__`, `__str__`) unless explicitly listed in `methods`.
    
    Parameters
    ----------
    decorator: Decorator
        An instance of the :class:`pydecorium.Decorator` class to apply to the methods.
        
    methods: list of str, optional
        A list of method names to which the decorator should be applied.
        If `None`, the decorator is applied to all methods of the class.
        Default value is `None`.

    Returns
    -------
    class_decorator: function
        A class decorator that applies the given decorator to specified methods.

    Raises
    ------
    TypeError
        - If `decorator` is not an instance of the :class:`pydecorium.Decorator` class.
        - If `methods` is provided and is not a list of strings.
    """
    if not isinstance(decorator, Decorator):
        raise TypeError("The parameter `decorator` must be an instance of the `Decorator` class.")
    
    if methods is not None:
        if not isinstance(methods, list) or not all(isinstance(method, str) for method in methods):
            raise TypeError("The `methods` parameter must be a list of strings or `None`.")

    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            # Check if the attribute is a regular function and matches the specified names
            if isinstance(attr_value, types.FunctionType) and (methods is None or attr_name in methods):
                setattr(cls, attr_name, decorator(attr_value))
        return cls

    return class_decorator
