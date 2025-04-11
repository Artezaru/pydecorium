print("# ======== pydecorium: Creating and using decorators ======== #")


#####
print("\n\nCreating a new decorator printing the function signature name")
print("------------------------")

from pydecorium import Decorator

class PrintFunctionName(Decorator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def _wrapper(self, func, *args, **kwargs):
        print(f"Function name: {self.get_signature_name(func)}")
        outputs = func(*args, **kwargs)
        return outputs




#####
print("\n\nUsing the decorator")
print("------------------------")

print_deco = PrintFunctionName(
    activated=True,  # Default value
    signature_name_format='{name}' # Default value
)

@print_deco
def my_function():
    pass

print("When running the function, the decorator will print the function name:")
my_function()

# Expected output:
# ----------------
# When running the function, the decorator will print the function name:
# Function name: my_function






#####
print("\n\nDeactivating the decorator")
print("------------------------")

@print_deco
def my_function():
    pass

print("Actually, the decorator is activated so the function name is printed:")
my_function()  # The decorator is activated
print_deco.set_activated(False)
print("Now, the decorator is deactivated so the function name is not printed:")
my_function()  # The decorator is deactivated
print_deco.set_activated(True)
print("The decorator is activated again so the function name is printed:")
my_function()  # The decorator is activated

# Expected output:
# ----------------
# Actually, the decorator is activated so the function name is printed:
# Function name: my_function
# Now, the decorator is deactivated so the function name is not printed:
# The decorator is activated again so the function name is printed:
# Function name: my_function





#####
print("\n\nDecorating methods")
print("------------------------")

class MyClass:
    @print_deco
    def my_method(self):
        pass

    @print_deco
    def my_second_method(self):
        pass

    def my_third_method(self):
        pass

my_class = MyClass()
print("When running the methods, the decorator will print the method name only for the decorated methods (first two):")
my_class.my_method()
my_class.my_second_method()
my_class.my_third_method()

# Expected output:
# ----------------
# When running the methods, the decorator will print the method name only for the decorated methods (first two):
# Function name: my_method
# Function name: my_second_method






#####
print("\n\nClass propagate")
print("------------------------")

from pydecorium import class_propagate

@class_propagate(print_deco, methods=['my_method', 'my_second_method'])
class MyClass:
    def my_method(self):
        pass

    def my_second_method(self):
        pass

    def my_third_method(self):
        pass

my_class = MyClass()
print("Same as before, the decorator will print the method name only for the decorated methods (first two):")
my_class.my_method()
my_class.my_second_method()
my_class.my_third_method()
print("The decorator is propagate among the given methods of the class")

# Expected output:
# ----------------
# Same as before, the decorator will print the method name only for the decorated methods (first two):
# Function name: my_method
# Function name: my_second_method
# The decorator is propagate among the given methods of the class






#####
print("\n\nSetting the fonction signature name format")
print("------------------------")

class MyClass:
    @print_deco
    def my_function(self):
        pass

class MyOtherClass:
    @print_deco
    def my_function(self):
        pass

print("By default, the decorator prints the function name so the two methods of different classes will have the same name:")
my_class = MyClass()
my_class.my_function()
my_other_class = MyOtherClass()
my_other_class.my_function()

# Expected output:
# ----------------
# By default, the decorator prints the function name so the two methods of different classes will have the same name:
# Function name: my_function
# Function name: my_function






#####
print("\n\nSolving the name signature issue")
print("------------------------")

print_deco.set_signature_name_format('{qualname}')

class MyClass:
    @print_deco
    def my_function(self):
        pass

class MyOtherClass:
    @print_deco
    def my_function(self):
        pass

print("Now, the decorator prints the function qualname so the two methods of different classes will have different names:")
my_class = MyClass()
my_class.my_function()
my_other_class = MyOtherClass()
my_other_class.my_function()

# Expected output:
# ----------------
# Now, the decorator prints the function qualname so the two methods of different classes will have different names:
# Function name: MyClass.my_function
# Function name: MyOtherClass.my_function