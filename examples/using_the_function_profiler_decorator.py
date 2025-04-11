print("# ======== pydecorium: Using the function profiler decorator ========")



#####
print("\n\nInstanciating the FunctionProfiler decorator")
print("------------------------")

from pydecorium.decorators import FunctionProfiler

function_profiler = FunctionProfiler(
    activated = True, # Default value
    signature_name_format = '{name}', # Default value
    report_format = "datetime" # Default value
)


#####
print("\n\nConnection the profiler utils to the decorator")
print("------------------------")

from pydecorium.decorators import Timer, Memory

function_profiler.connect_profiler_utils([Timer, Memory])




#####
print("\n\nUsing the FunctionProfiler decorator")
print("------------------------")

import time

@function_profiler
def my_function():
    pass

@function_profiler
def my_second_function():
    time.sleep(0.1)
    pass

print("When running the function, the decorator will store the time of execution and the memory usage because the Timer and Memory utils are connected:")
my_function()
my_second_function()
my_function()

print("print the decorator to generate the report:")
print(function_profiler)

# Expected output:
# ----------------
# When running the function, the decorator will store the time of execution and the memory usage because the Timer and Memory utils are connected:
# print the decorator to generate the report:
# [2025-01-21 19:30:07.407461] - [my_function] - runtime : 0h 0m 0.0001s - memory usage : 0MB 0KB 0B1
# [2025-01-21 19:30:07.407583] - [my_second_function] - runtime : 0h 0m 0.1000s - memory usage : 0MB 0KB 0B
# [2025-01-21 19:30:07.407631] - [my_function] - runtime : 0h 0m 0.0000s - memory usage : 0MB 0KB 0B







#####
print("\n\nInitializing the FunctionProfiler decorator")
print("------------------------")

function_profiler.initialize()

print("When initializing the decorator, the data collected are removed but the utils are already connected:")
my_function()
my_second_function()
my_second_function()

print(function_profiler)

# Expected output:
# ----------------
# When initializing the decorator, the data collected are removed but the utils are already connected:
#[2025-01-21 19:33:05.796596] - [my_function] - runtime : 0h 0m 0.0000s - memory usage : 0MB 0KB 0B
#[2025-01-21 19:33:05.796645] - [my_second_function] - runtime : 0h 0m 0.1000s - memory usage : 0MB 0KB 0B
#[2025-01-21 19:33:05.796685] - [my_second_function] - runtime : 0h 0m 0.1000s - memory usage : 0MB 0KB 0B







#####
print("\n\nChanging the report format")
print("------------------------")

function_profiler.report_format = "function"

print(function_profiler)

# Expected output:
# ----------------
#[my_function]
#    [2025-01-21 19:33:05.796596] - runtime : 0h 0m 0.0000s - memory usage : 0MB 0KB 0B
#[my_second_function]
#    [2025-01-21 19:33:05.796645] - runtime : 0h 0m 0.1000s - memory usage : 0MB 0KB 0B
#    [2025-01-21 19:33:05.796685] - runtime : 0h 0m 0.1000s - memory usage : 0MB 0KB 0B

function_profiler.report_format = "cumulative"

print(function_profiler)

# Expected output:
# ----------------
#[my_function] - 1 calls - runtime : 0h 0m 0.0000s - memory usage : 0MB 0KB 0B
#[my_second_function] - 2 calls - runtime : 0h 0m 0.2000s - memory usage : 0MB 0KB 0B

