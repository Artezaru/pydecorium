How to use a decorator
======================

Basic usage
-----------

After you have implemented a decorator using the documentation :doc:`./create_decorator`, you can use it to decorate a function.
To apply a decorator to a function, simply add the decorator to the function definition.

To explain how to use a decorator, we will use the decorator ``PrintFunctionName`` created in the documentation :doc:`./create_decorator`.
This decorator prints the name of the function before its execution.

.. code-block:: python

    print_deco = PrintFunctionName(activated=True, signature_name_format='{name}')

    @print_deco
    def my_function():
        print("Hello world!")

When the function is called, the decorator will be executed and the result will be:

.. code-block:: console

    Function name: my_function
    Hello world!

The package ``pydecorium`` provides the possibility to activate or deactivate a decorator using the parameter ``activated`` (see :doc:`../api_doc/decorator`).
This parameter is set to ``True`` by default.
When the parameter is set to ``False``, the decorator is not executed and the function is called as if it was not decorated.

.. code-block:: python

    @print_deco
    def my_function():
        print("Hello world!")

    my_function()  # The decorator is activated
    print_deco.set_activated(False)
    my_function()  # The decorator is deactivated
    print_deco.set_activated(True)
    my_function()  # The decorator is activated

The result will be:

.. code-block:: console

    Function name: my_function
    Hello world!
    Hello world!
    Function name: my_function
    Hello world!

Class decoration
----------------

Decorators must decorate a function or a method.
To decorate several methods of a class, you can use the decorator on each method like this:

.. code-block:: python

    class MyClass:
        @print_deco
        def my_method(self):
            print("Hello world! (1)")

        @print_deco
        def my_second_method(self):
            print("Hello world! (2)")

        def my_third_method(self):
            print("Hello world! (3)")

    my_class = MyClass()
    my_class.my_method()
    my_class.my_second_method()
    my_class.my_third_method()

The result will be:

.. code-block:: console

    Function name: my_method
    Hello world! (1)
    Function name: my_second_method
    Hello world! (2)
    Hello world! (3)

To facilitate the decoration of methods of a class, you can use the fonction :func:`pydecorium.class_propagate`.

.. code-block:: python

    from pydecorium import class_propagate

    @class_propagate(print_deco, methods=['my_method', 'my_second_method'])
    class MyClass:
        def my_method(self):
            print("Hello world! (1)")

        def my_second_method(self):
            print("Hello world! (2)")

        def my_third_method(self):
            print("Hello world! (3)")

    my_class = MyClass()
    my_class.my_method()
    my_class.my_second_method()
    my_class.my_third_method()

The result will be exactly the same as the previous example.
If all methods of the class must be decorated, you can set the parameter ``methods`` to ``None`` (default value).

Differenciate the functions/methods
-----------------------------------

When a decorator is applied to several functions or methods, it is sometimes useful to differentiate the functions or methods if their names are the same.

Lets consider the following example:

.. code-block:: python

    class MyClass:
        @print_deco
        def my_function(self):
            print("Hello world! (1)")

    class MyOtherClass:
        @print_deco
        def my_function(self):
            print("Hello world! (2)")

    my_class = MyClass()
    my_class.my_function()
    my_other_class = MyOtherClass()
    my_other_class.my_function()

The result will be:

.. code-block:: console

    Function name: my_function
    Hello world! (1)
    Function name: my_function
    Hello world! (2)

We see here that the decorator does not differentiate the functions because they have the same name.
To differentiate the functions, you can use the parameter ``signature_name_format`` from the decorator (see :doc:`../api_doc/decorator`).
For example, you can fix the signature name as the ``qualname`` of the function:

.. code-block:: python

    print_deco.set_signature_name_format('{qualname}')

    class MyClass:
        @print_deco
        def my_function(self):
            print("Hello world! (1)")

    class MyOtherClass:
        @print_deco
        def my_function(self):
            print("Hello world! (2)")

    my_class = MyClass()
    my_class.my_function()
    my_other_class = MyOtherClass()
    my_other_class.my_function()

The result will be:

.. code-block:: console

    Function name: MyClass.my_function
    Hello world! (1)
    Function name: MyOtherClass.my_function
    Hello world! (2)
