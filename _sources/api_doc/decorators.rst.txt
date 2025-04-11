pydecorium.decorators
=====================

``decorators`` is a sub-module of ``pydecorium`` that provides a collection of decorators for use in Python programming.

This sub-module is composed of the following classes:

- ``pydecorium.decorators.ProfilerUtils`` class is the base class for the utils decorators profiling functions and methods.
- ``pydecorium.decorators.Timer`` and ``pydecorium.decorators.Memory`` are utils decorators that measure the runtime and memory usage of a function or a method.
- ``pydecorium.decorators.FunctionProfiler`` is a decorator using the utils decorators to profile functions and methods and reporting the results as logs.

.. toctree::
    :maxdepth: 1
    :caption: pydecorium.decorators API:

    ./profiler_utils.rst
    ./timer.rst
    ./memory.rst
    ./function_profiler.rst

The user guide for the implemented decorators is available in the section :doc:`../usage_doc/implemented_decorators`.

