How to create a decorator
=========================

Generalities
------------

To create a new decorator, first import the :class:`pydecorium.Decorator` class.

.. code-block:: python

    from pydecorium import Decorator

Then, create a new class that inherits from the :class:`pydecorium.Decorator` class and add the initialization method.
The new class should implement the ``_wrapper`` method, which is called 
when the decorated function is called. The ``_wrapper`` method should be defined as follows:

.. code-block:: python

    class MyDecorator(Decorator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def _wrapped(self, func, *args, **kwargs):
            self.pre_execute()
            outputs = func(*args, **kwargs)
            self.post_execute()
            return outputs

The ``_wrapper`` can access the signature name of the given function ``func`` using the method ``self.get_signature_name(func)``.

Example
-------

The following example shows how to create a simple decorator that prints the name of the function before its execution.

.. code-block:: python

    class PrintFunctionName(Decorator):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
   
        def _wrapper(self, func, *args, **kwargs):
            print(f"Function name: {self.get_signature_name(func)}")
            outputs = func(*args, **kwargs)
            return outputs

To use the ``PrintFunctionName`` decorator, simply decorate a function with it.
More information on how to use a decorator can be found in the documentation :doc:`./use_decorator`.