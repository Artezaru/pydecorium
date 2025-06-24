How to create a profiler utils decorator
========================================

To create a new profiler utils decorator for the :class:`pydecorium.decorators.FunctionProfiler` decorator, you need to create a class that inherits from the base class :class:`pydecorium.decorators.ProfilerUtils`.

First import the class ``ProfilerUtils`` from the module ``pydecorium.decorators``:

.. code-block:: python

    from pydecorium.decorators import ProfilerUtils

Then create a new class that inherits from the class ``ProfilerUtils``:

.. code-block:: python

    class MyProfilerUtils(ProfilerUtils):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

Then you need to add the following methods and attributes:

- ``data_name``: This attribute is a string that represents the name of the data that will be profiled.
- ``pre_execute``: This method is called before the execution of the decorated function. It arguments are the function and the arguments of the function.
- ``post_execute``: This method is called after the execution of the decorated function. It arguments are the function and the outputs of the function.
- ``handle_result``: This method is called after the execution of the decorated function and has not arguments. It should return the raw data of the profiler utils.
- ``string_value``: This method takes the raw data of the profiler utils as argument and returns a string representation of the profiler utils.

Example
-------

The following example shows how to create a simple profiler utils decorator that measures the runtime of a function.
This example is similar than :class:`pydecorium.decorators.Timer` decorator.

.. code-block:: python

    import time

    class MyProfilerUtils(ProfilerUtils):

        data_name = "runtime"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
   
        def pre_execute(self, func, *args, **kwargs):
            self.tic = time.time()

        def post_execute(self, func, outputs):
            self.toc = time.time()

        def handle_result(self):
            return self.toc - self.tic

        def string_value(self, raw_data):
            return f"{raw_data:.2f} seconds"