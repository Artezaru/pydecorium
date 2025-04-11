import re
import functools

class Decorator(object):
    """
    Base class for decorators.

    The subclasses must implement the ``_wrapper`` method with the following signature:

    .. code-block:: python

        def _wrapper(self, func, *args, **kwargs):
            pre_execute()
            outputs = func(*args, **kwargs)
            post_execute()
            return outputs

    The subclasses can access several attributes about the function to decorate:
    
    - function_signature_name: The signature name of the function. The signature name can be set using the signature_name_format attribute.
    
    Parameters
    ----------
    activated: bool, optional
        The activation status of the decorator.
        Default value is True

    signature_name_format: str, optional
        The format of the signature name to display. (see :meth:`set_signature_name_format`)
        Default value is "{name}"
    """
    
    correct_signature_name_format_args = ["name", "module", "qualname"]

    def __init__(self, *, 
        activated: bool = True,
        signature_name_format: str = "{name}",
        ):
        self._activated = True
        self._signature_name_format = signature_name_format

    # Properties getters and setters
    @property
    def activated(self) -> bool:
        """
        Getter and setter for the activation status of the decorator.

        Parameters
        ----------
        activated: bool
            The activation status of the decorator.

        Raises
        ------
        TypeError
            If the given argument is not a booleen.
        """
        return self._activated

    @activated.setter
    def activated(self, activated: bool):
        if not isinstance(activated, bool):
            raise TypeError("Parameter activated is not a booleen.")
        self._activated = activated
    
    @property
    def signature_name_format(self) -> str:
        """
        Getter and setter for the format of the signature name to display.

        Parameters
        ----------
        signature_name_format: str
            The format of the signature name to display.
        
        Raises
        ------
        ValueError
            If the given signature name format is not correct.
        TypeError
            If the given argument is not a string.
        """
        return self._signature_name_format
    
    @signature_name_format.setter
    def signature_name_format(self, signature_name_format: str):
        if not self.check_signature_name_format(signature_name_format):
            raise ValueError("The given name format is not correct.")
        self._signature_name_format = signature_name_format
    
    # Decorator activation and deactivation (other way around)
    def is_activated(self) -> bool:
        """ 
        Returns decorator activation status.

        .. note:: 

            The activation status can also be get using the activated property: decorator.activated

        .. seealso::
        
            - :meth:`is_deactivated` : Returns decorator deactivation status.
            - :meth:`set_activated` : Sets the decorator activation status.
        
        Returns
        -------
        activated: bool
            If the decorator is activated.
        """
        return self.activated

    def is_deactivated(self) -> bool:
        """
        Returns decorator deactivation status.

        .. note:: 

            The deactivation status can also be get using the activated property: not decorator.activated

        .. seealso::

            - :meth:`is_activated` : Returns decorator activation status.
            - :meth:`set_deactivated` : Sets the decorator deactivation status

        Returns
        -------
        deactivated: bool
            If the decorator is deactivated.
        """
        return not self.activated

    def set_activated(self, activated: bool = True) -> None:
        """
        Sets the decorator activation status.

        .. note::

            The activation status can also be set using the activated property: decorator.activated = True

        .. seealso::
        
            - :meth:`is_activated` : Returns decorator activation status.
            - :meth:`set_deactivated` : Sets the decorator deactivation status.
        
        Parameters
        ----------
        activated: bool, optional
            The activation status to apply to the decorator.
            Default value is True
        
        Raises
        ------
        TypeError
            If the given argument is not a booleen.
        """
        self.activated = activated

    def set_deactivated(self, deactivated: bool = True) -> None:
        """
        Sets the decorator deactivation status.

        .. note::

            The deactivation status can also be set using the activated property: decorator.activated = False

        .. seealso::
        
            - :meth:`is_deactivated` : Returns decorator deactivation status.
            - :meth:`set_activated` : Sets the decorator activation status.

        Parameters
        ----------
        deactivated: bool, optional
            The deactivation status to apply to the decorator.
            Default value is True

        Raises
        ------
        TypeError
            If the given argument is not a booleen.
        """
        self.activated = not deactivated

    # Decorator signature name formatting
    def set_signature_name_format(self, signature_name_format: str) -> None:
        """
        Sets the signature name format of the decorator.

        .. note::
        
            The signature name format can be set using the signature_name_format property: decorator.signature_name_format = "{name}"
        
        .. important::

            The signature name can be formatted using the following arguments:

            - {name}: The name of the function
            - {module}: The module of the function
            - {qualname}: The qualname of the function

            Example of valid signature_name_format:

            - "{name}": Display the name of the function.
            - "{module}.{qualname}": Display the module and qualname of the function.
            - "Function {name} from {module}": Display a custom message with the function name and module.
            - "{name} and \\{other}": Display the string "{other}" (use \\ to escape the brackets).
            - "\\{other {name} other}": Display the string "{other {name} other}" (use \\ to escape the brackets).

            Example of invalid signature_name_format:

            - "{other}": The format argument "other" is not valid.
            - "{name} and {qualname": The brackets are not correctly closed.


        .. seealso::

            - :meth:`get_signature_name_format` : Allows to get the format of the signature name of the decorator.

        Parameters
        ----------
        signature_name_format: str
            The format of the signature name to display.
    
        Raises
        ------
        ValueError
            If the given signature name format is not correct.
        TypeError
            If the given argument is not a string.
        """
        self.signature_name_format = signature_name_format

    def get_signature_name_format(self) -> str:
        """
        Get the signature name format of the decorator.

        .. note::
        
            The signature name format can be get using the signature_name_format property: decorator.signature_name_format
        

        .. seealso::

            - :meth:`set_signature_name_format` : Allows to set the format of the signature name of the decorator.
        
        Returns
        -------
        signature_name_format: str
            The format of the signature name to display.
        """
        return self.signature_name_format
    
    def get_signature_name(self, func) -> str:
        """
        Get the signature name of the function.

        Parameters
        ----------
        func: function
            The function to get the signature name from.
        
        Returns
        -------
        signature_name: str
            The signature name of the function.
        """
        pattern = r'(?<!\\)\{(.*?)(?<!\\)\}'
        # Replace the format with the function attributes
        def replace(match, format_args: dict) -> str:
            key = match.group(1)
            return format_args.get(key, f"{{{key}}}") # Return the key if not found
        # Get the function attributes
        format_args = {
            "name": func.__name__,
            "module": func.__module__,
            "qualname": func.__qualname__,
        }
        # Replace the format with the function attributes
        formatted_name = re.sub(pattern, lambda match: replace(match, format_args), self.signature_name_format)
        formatted_name = formatted_name.replace(r'\{', '{').replace(r'\}', '}')
        return formatted_name
        
    def _check_accolades(self, signature_name_format: str) -> bool:
        """
        Check if the accolades are correctly closed for the signature name format.

        .. seealso::
        
            - :meth:`check_signature_name_format` : Check if the signature name format is correct.

        Parameters
        ----------
        signature_name_format: str
            The signature name format to check.
        
        Returns
        -------
        is_correct: bool
            If the accolades are correctly closed.

        Raises
        ------
        TypeError
            If the given argument is not a string.
        """
        if not isinstance(signature_name_format, str):
            raise TypeError("Parameter signature_name_format is not a string.")
        stack = []
        for char in signature_name_format:
            if char == "{":
                stack.append("{")
            elif char == "}":
                if len(stack) == 0:
                    return False
                stack.pop()
        return len(stack) == 0

    def check_signature_name_format(self, signature_name_format: str) -> bool:
        """
        Check if the signature name format is correct.

        Parameters
        ----------
        signature_name_format: str
            The signature name format to check.
    
        Returns
        -------
        is_correct: bool
            If the signature name format is correct.

        Raises
        ------
        TypeError
            If the given argument is not a string.
        """
        if not isinstance(signature_name_format, str):
            raise TypeError("Parameter signature_name_format is not a string.")
        if not self._check_accolades(signature_name_format):
            return False
        pattern = r'(?<!\\)\{(.*?)(?<!\\)\}'
        matches = re.findall(pattern, signature_name_format)
        for match in matches:
            if match not in self.correct_signature_name_format_args:
                return False
        return True

    # Decorator wrapper
    def __call__(self, func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if self._activated:
                return self._wrapper(func, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapped

    # To be implemented in subclasses
    def _wrapper(self, func, *args, **kwargs):
        """
        Wrapper method to be implemented in subclasses.
        """
        raise NotImplementedError("Method _wrapper must be implemented in subclasses.")


    