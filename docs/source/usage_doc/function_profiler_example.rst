FunctionProfiler Usage
======================

The :class:`pydecorium.decorators.FunctionProfiler` decorator is used to profile some data about the function execution as the runtime, the memory usage, etc.
``FunctionProfiler`` is a sub-class of the class :class:`pydecorium.Decorator`.

First we need to import the ``FunctionProfiler`` decorator with the following command:

.. code-block:: python

    from pydecorium.decorators import FunctionProfiler

Then we can connect some :class:`pydecorium.decorators.ProfilerUtils` decorators to the ``FunctionProfiler`` decorator.
By connecting a ``ProfilerUtils`` decorator to the ``FunctionProfiler`` decorator, the ``ProfilerUtils`` decorator will be use by the ``FunctionProfiler`` decorator to profile a given data about the function execution.
If several ``ProfilerUtils`` decorators are connected to the ``FunctionProfiler`` decorator, all the connected ``ProfilerUtils`` decorators will be used to profile the function execution.

In this example, we will connect the :class:`pydecorium.decorators.Timer` and :class:`pydecorium.decorators.Memory` decorators to the ``FunctionLogger`` decorator.
To do this, we use the profiler_utils argument of the ``FunctionProfiler`` decorator.
We can also use the method ``connect_profiler_utils`` of the ``FunctionProfiler`` decorator as follows:

.. code-block:: python

    from pydecorium.decorators import Timer, Memory

    function_profiler = FunctionProfiler(
        activated=True, 
        signature_name_format='{name}', 
        profiler_utils=[Timer, Memory],
        report_format='datetime')
    
    # OR 
    fonction_profiler.connect_profiler_utils([Timer, Memory])

If we try to connect a ``ProfilerUtils`` decorator already connected to the ``FunctionProfiler`` decorator, the ``ProfilerUtils`` decorator will be connected only once.

Then we can use the ``FunctionProfiler`` as describe in the documentation :doc:`./use_decorator`.

.. code-block:: python

    @function_profiler
    def example_function():
        import time
        time.sleep(10)
        return [i for i in range(1000000)]

    @function_profiler
    def other_example_function():
        import time
        time.sleep(5)
        return [i for i in range(5000)]

    example_function()
    example_function()
    other_example_function()
    example_function()

To see the report of the ``FunctionProfiler`` decorator, just print ``function_profiler``.

.. code-block:: python

    print(function_profiler)

The output when printing the ``function_profiler`` object depends on the ``report_format`` attribute of the ``FunctionProfiler`` object.


Selecting the report format
----------------------------

To change the format of the string reporting the function execution, use the method :func:`pydecorium.decorators.FunctionProfiler.set_report_format`.

If the ``report_format`` is set to "datetime", the output will be:

.. code-block:: console

    [2025-01-20 18:23:08.696188] - [example_function] - runtime : 0h 0m 10.0217s - memory usage : 38MB 320KB 0B
    [2025-01-20 18:23:18.723690] - [example_function] - runtime : 0h 0m 10.0239s - memory usage : 36MB 256KB 0B
    [2025-01-20 18:23:28.752144] - [other_example_function] - runtime : 0h 0m 5.0006s - memory usage : 0MB 0KB 0B
    [2025-01-20 18:23:33.753020] - [example_function] - runtime : 0h 0m 10.0304s - memory usage : 28MB 512KB 0B

If the ``report_format`` is set to "function", the output will be:

.. code-block:: console

    [example_function]
        [2025-01-20 18:36:44.569795] - runtime : 0h 0m 10.0225s - memory usage : 38MB 380KB 0B
        [2025-01-20 18:36:54.597933] - runtime : 0h 0m 10.0218s - memory usage : 37MB 256KB 0B
        [2025-01-20 18:37:09.626250] - runtime : 0h 0m 10.0193s - memory usage : 28MB 0KB 0B
    [other_example_function]
            [2025-01-20 18:37:04.625249] - runtime : 0h 0m 5.0006s - memory : 0MB 0KB 0B

If the ``report_format`` is set to "cumulative", the output will be:

.. code-block:: console

    [example_function] - 3 calls - runtime : 0h 0m 30.0666s - memory usage : 103MB 232KB 0B
    [other_example_function] - 1 calls - runtime : 0h 0m 5.0008s - memory usage : 0MB 0KB 0B

Add new profiler utils
----------------------

To add a new profiler utils to the ``FunctionProfiler`` decorator, refer to the documentation :doc:`./create_profiler_utils`.
