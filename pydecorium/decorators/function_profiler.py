from ..decorator import Decorator
from .profiler_utils import ProfilerUtils
from .timer import Timer
from .memory import Memory

from typing import List, Union, Type, Callable, Dict
import datetime

class FunctionProfiler(Decorator):
    r"""
    ``FunctionProfiler`` is a :class:`pydecorium.Decorator` that profile the execution of a function such as execution time, memory usage etc.
    
    Several profiler utils :class:`pydecorium.decorators.ProfilerUtils` can be connected to the ``FunctionProfiler`` according to the user's needs.
    Each profiler utils is used to collect a specific data during the function execution.
    For example, the :class:`pydecorium.decorators.Timer` is used to collect the execution time of the function and the :class:`pydecorium.decorators.Memory` is used to collect the memory usage of the function.

    The various functions and methods decorated with the ``FunctionProfiler`` are identified by their func pointer.
    When the report of the profiled data is generated, the function signature name is used to help the user to identify the profiled data.
    The `signature_name_format` attribute of this decorator can be used to customize the function signature name (see :class:`pydecorium.Decorator`).

    The report of the profiled data can be formatted in three different ways: "datetime", "function", "cumulative".

    Parameters
    ----------
    profiler_utils : Union[Type, List[Type]]
        The list of sub-classes of the ``ProfilerUtils`` class to connect to the ``FunctionProfiler``.
        Default is None.
    report_format : str
        The format of the string to report the profiled data. (see :meth:`pydecorium.decorators.FunctionProfiler.set_report_format`).
        The valid values are: "datetime", "function", "cumulative".
        Default is "datetime". 

    Attributes
    ----------
    report_format : str
        The format of the string to report the profiled data. (see :meth:`pydecorium.decorators.FunctionProfiler.set_report_format`).

    profiled_functions : List[Callable]
        The list containing the functions/methods actually profiled by the ``FunctionProfiler``.

    profiled_functions_signature_name : List[str]
        The list containing the signature name of the functions/methods actually profiled by the ``FunctionProfiler``.

    connected_profiler_utils : List[ProfilerUtils]
        The list of the connected ``ProfilerUtils`` to the ``FunctionProfiler``.

    profiled_data : List[List]
        The list of the profiled data containing the datetime, the index of the function and the data collected by the connected ``ProfilerUtils``. The data are a dictionary with the index of the connected ``ProfilerUtils`` as key and the data collected as value.

    report : str
        The string reporting the profiled data according to the selected ``report_format``.
    """
    correct_report_format = ["datetime", "function", "cumulative"]

    def __init__(self, profiler_utils: Union[Type, List[Type]] = None,
                 report_format: str = "datetime", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.disconnect_all()
        self.connect_profiler_utils(profiler_utils)
        self.report_format = report_format

    # Properties getters and setters
    @property
    def report_format(self) -> str:
        return self._report_format

    @report_format.setter
    def report_format(self, report_format: str) -> None:
        if not isinstance(report_format, str):
            raise TypeError("The report_format must be a string.")
        if report_format not in self.correct_report_format:
            raise ValueError(f"The report_format must be one of the following: {self.correct_report_format}.")
        self._report_format = report_format

    @property
    def profiled_functions():
        return self._profiled_functions

    @property
    def profiled_functions_signature_name():
        return [self.get_signature_name(func) for func in self._profiled_functions]

    @property
    def connected_profiler_utils():
        return self._connected_profiler_utils

    @property
    def profiled_data():
        return self._profiled_data

    # Decorator log format (other way around)
    def set_report_format(self, report_format: str) -> None:
        r"""
        Sets the ``report_format`` of the ``FunctionProfiler``.
        The report format is used to format the string to report the profiled data.

        .. note:: 

            The format can also be set using the ``report_format`` attribute.

        .. important::

            The correct format are: "datetime", "function", "cumulative". (see below)

            If the ``report_format`` is set to "datetime", the reported string will be formatted as follows:

            .. code-block:: console
            
                [datetime] - [function_signature_name] - data_name : data - other_data_name : other_data
                [datetime] - [other_function_signature_name] - data_name : data - other_data_name : other_data
                [datetime] - [function_signature_name] - data_name : data - other_data_name : other_data
                
            If the ``report_format`` is set to "function", the reported string will be formatted as follows:

            .. code-block:: console

                [function_signature_name]
                    [datetime] - data_name : data - other_data_name : other_data
                    [datetime] - data_name : data - other_data_name : other_data
                [other_function_signature_name]
                    [datetime] - data_name : data - other_data_name : other_data
                    [datetime] - data_name : data - other_data_name : other_data

            If the ``report_format`` is set to "cumulative", the reported string will be formatted as follows:

            .. code-block:: console

                [function_signature_name] - N calls - data_name : cumulative_data - other_data_name : cumulative_other_date
                [other_function_signature_name] - N calls - data_name : cumulative_data - other_data_name : cumulative_other_date

            .. warning::
                The `cumulative` reported format can't be use if the linked ``FunctionProfiler`` returns non-numeric data.

        Parameters
        ----------
        report_format : str
            The format of the string to report the profiled data.

        Raises
        ------
        TypeError
            If the report_format is not a string.
        ValueError
            If the report_format is not in the correct log format.
        """
        self.report_format = report_format

    def get_report_format(self) -> str:
        r"""
        Gets the format of the string to report the profiled data.

        .. note::
        
            The reported format can also be get using the 'report_format' attribute.

        Returns
        -------
        str
            The format of the string to report the profiled data.
        """
        return self.report_format

    def extract_loggeg_functions(self) -> List[Callable]:
        r"""
        Extracts the list containing the functions/methods actually profiled by the ``FunctionProfiler``.
        The list is sorted by the order of the function calls.

        .. note::

            The list can also be get using the 'profiled_functions' attribute.

        Returns
        -------
        List[Callable]
            The list containing the functions/methods actually profiled by the ``FunctionProfiler``.
        """
        return self.profiled_functions

    def extract_loggeg_functions_signature_name(self) -> List[str]:
        r"""
        Extracts the list containing the signature name of the functions/methods actually profiled by the ``FunctionProfiler``.
        The list is sorted by the order of the function calls.

        .. note::

            The list can also be get using the 'profiled_functions_signature_name' attribute.
        
        Returns
        -------
        List[str]
            The list containing the signature name of the functions/methods actually profiled by the ``FunctionProfiler``.
        """
        return self.profiled_functions_signature_name

    def extract_connected_profiler_utils(self) -> List[ProfilerUtils]:
        r"""
        Extracts the list of the connected ``ProfilerUtils`` to the ``FunctionProfiler``.
        Note that the list contains the instances of the connected ``ProfilerUtils`` and not the classes.

        .. note::

            The list can also be get using the 'connected_profiler_utils' attribute.

        Returns
        -------
        List[ProfilerUtils]
            The list of the connected ``ProfilerUtils`` to the ``FunctionProfiler``.
        """
        return self.connected_profiler_utils

    def extract_profiled_data(self) -> List[List]:
        r"""
        Extracts the list of the profiled data containing the datetime, the function and the data collected by the connected ``ProfilerUtils``.
        The list is sorted by the order of the function calls.

        .. note::

            The list can also be get using the 'profiled_data' attribute.

        The structure of the list is as follows:

        .. code-block:: python

            profiled_data = [[datetime, function_index, {utils_index: data, utils_index: data, ...}], ...]

        Returns
        -------
        List[List]
            The list of the profiled data containing the datetime, the index of the function and the data collected by the connected ``ProfilerUtils``.
        """
        return self.profiled_data

    def extract_profiled_data_reorganized_by_function(self) -> Dict[int, List[List]]:
        r"""
        Reorganizes the profiled data by function.

        For example, the profiled data:

        .. code-block:: python

            data = [[datetime, function_index_1, {utils_index: data, utils_index: data, ...}],
                    [datetime, function_index_2, {utils_index: data, utils_index: data, ...}],
                    [datetime, function_index_1, {utils_index: data, utils_index: data, ...}], ...]
        
        becomes:

        .. code-block:: python

            data = {function_index_1: [[datetime, {utils_index: data, utils_index: data, ...}],
                                    [datetime, {utils_index: data, utils_index: data, ...}], ...],
                    function_index_2: [[datetime, {utils_index: data, utils_index: data, ...}], ...], ...}

        Returns
        -------
        Dict[int, List[List]]
            The profiled data reorganized by function.
        """
        reorganized_data = {}
        for log in self._profiled_data:
            function_index = log[1]
            if function_index not in reorganized_data.keys():
                reorganized_data[function_index] = []
            reorganized_data[function_index].append([log[0], log[2]])
        return reorganized_data

    # FunctionProfiler methods
    def initialize(self) -> None:
        r"""
        Initializes the ``FunctionProfiler`` by removing all the profiled data.

        The connected profiler utils are not removed.
        """
        self._profiled_data = []
        self._profiled_functions = []

    def disconnect_all(self) -> None:
        r"""
        Disconnects all the profiler utils connected to the ``FunctionProfiler``.

        .. note::

            The profiled data are removed.
        """
        self._connected_profiler_utils = []
        self.initialize()
    
    def connect_profiler_utils(self, profiler_utils: Union[Type, List[Type]] = None) -> None:
        r"""
        Connects a sub-class of the ``ProfilerUtils`` class to the ``FunctionProfiler``.
        If a logger utils is None, it will be ignored.

        Parameters
        ----------
        profiler_utils : Union[Type, List[Type]]
            The sub-class of the ``ProfilerUtils`` class to connect to the ``FunctionProfiler``.

        Raises
        ------
        TypeError
            If the logger is not an instance of ``ProfilerUtils`` or a list of ``FunctionProfiler``.
        """
        # Recursively connect the logger
        if isinstance(profiler_utils, list):
            for utils in profiler_utils:
                self.connect_profiler_utils(utils)
        else:
            if profiler_utils is None:
                return
            if not issubclass(profiler_utils, ProfilerUtils):
                raise TypeError("The profiler utils must be a sub-class of ProfilerUtils.")
            # Testing if the profiler utils is already connected
            if any(isinstance(utils, profiler_utils) for utils in self._connected_profiler_utils):
                return
            self._connected_profiler_utils.append(profiler_utils()) # Add an instance of the profiler utils. It will be used to collect the data.
    
    # Wrapper method
    def _wrapper(self, func, *args, **kwargs):
        r"""
        Compute the profiled data of the function execution.
        """
        date = datetime.datetime.now()
        data = {}
        # Test if the function is already profiled
        function_index = 0
        while (function_index < len(self._profiled_functions)) and (self._profiled_functions[function_index] is not func):
            function_index += 1
        if function_index == len(self._profiled_functions):
            self._profiled_functions.append(func)
        # Pre-execute
        for utils_index, utils in enumerate(self._connected_profiler_utils):
            utils.pre_execute(func, *args, **kwargs)
        # Execute the function
        outputs = func(*args, **kwargs)
        # Post-execute
        for utils_index, utils in enumerate(self._connected_profiler_utils):
            utils.post_execute(func, *args, **kwargs)
        # Handle the logged data
        for utils_index, utils in enumerate(self._connected_profiler_utils):
            data[utils_index] = utils.handle_result()
        # Append the logged data
        self._profiled_data.append([date, function_index, data])        
        return outputs

    # Report methods
    def generate_report_datetime(self) -> str:
        r"""
        Generates the report of the ``FunctionProfiler`` in the "datetime" format.

        .. seealso::

            :func:`pydecorium.decorators.FunctionProfiler.set_report_format()`

        Returns
        -------
        str
            The report of the ``FunctionProfiler`` in the "datetime" format.

        """
        report = ""
        for log in self._profiled_data:
            # Extract the data
            date = log[0]
            function_index = log[1]
            data = log[2]
            # Extract the function signature name
            function_signature_name = self.get_signature_name(self._profiled_functions[function_index])
            report += f"[{date}] - [{function_signature_name}]"
            # Writting the data
            for utils_index, data_value in data.items():
                utils = self._connected_profiler_utils[utils_index]
                report += f" - {utils.string_result(data_value)}"
            report += "\n"
        return report

    def generate_report_function(self) -> str:
        r"""
        Generates the report of the ``FunctionProfiler`` in the "function" format.

        .. seealso::

            :func:`pydecorium.decorators.FunctionProfiler.set_report_format()`

        Returns
        -------
        str
            The report of the ``FunctionProfiler`` in the "function" format.
        """
        report = ""
        # Reorganize the data by function
        reorganized_data = self.extract_profiled_data_reorganized_by_function()
        # Write the report
        for function_index, logs in reorganized_data.items():
            # Extract the function signature name
            function_signature_name = self.get_signature_name(self._profiled_functions[function_index])
            report += f"[{function_signature_name}]\n"
            # Read the data
            for log in logs:
                date = log[0]
                data = log[1]
                report += f"\t[{date}]"
                # Writting the data
                for utils_index, data_value in data.items():
                    utils = self._connected_profiler_utils[utils_index]
                    report += f" - {utils.string_result(data_value)}"
                report += "\n"
        return report

    def generate_report_cumulative(self) -> str:
        r"""
        Generates the report of the ``FunctionProfiler`` in the "cumulative" format.

        .. seealso::

            :func:`pydecorium.decorators.FunctionProfiler.set_report_format()`

        Returns
        -------
        str
            The report of the ``FunctionProfiler`` in the "cumulative" format.
        """
        report = ""
        # Reorganize the data by function
        reorganized_data = self.extract_profiled_data_reorganized_by_function()
        # Write the report
        for function_index, logs in reorganized_data.items():
            # Extract the function signature name
            function_signature_name = self.get_signature_name(self._profiled_functions[function_index])
            report += f"[{function_signature_name}]"
            # Read the data
            calls = len(logs)
            cumulative_data = {}
            for log in logs:
                data = log[1]
                for utils_index, data_value in data.items():
                    if utils_index not in cumulative_data.keys():
                        cumulative_data[utils_index] = 0
                    cumulative_data[utils_index] += data_value
            report += f" - {calls} calls"
            for utils_index, data_value in cumulative_data.items():
                utils = self._connected_profiler_utils[utils_index]
                report += f" - {utils.string_result(data_value)}"
            report += "\n"
        return report

    def generate_report(self) -> str:
        """
        Generates the report of the ``FunctionProfiler`` according to the log format.

        .. seealso::

            :func:`pydecorium.decorators.FunctionProfiler.set_report_format()`

        Returns
        -------
        str
            The report of the ``FunctionProfiler`` in the specified log format.

        """
        if self.report_format == "datetime":
            return self.generate_report_datetime()
        elif self.report_format == "function":
            return self.generate_report_function()
        elif self.report_format == "cumulative":
            return self.generate_report_cumulative()
    
    def write_report(self, file_path: str) -> None:
        """
        Writes the report of the ``FunctionProfiler`` in a file at the specified path according to the selected ``report_format``.

        Parameters
        ----------
        file_path : str
            The path of the file where the report will be written.
        """
        with open(file_path, "w") as file:
            file.write(self.generate_report())

    def __str__(self) -> str:
        return self.generate_report()

    def __repr__(self) -> str:
        return self.generate_report()