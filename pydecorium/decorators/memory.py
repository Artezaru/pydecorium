from .profiler_utils import ProfilerUtils
import psutil

class Memory(ProfilerUtils):
    """
    Timer ``Memory`` is a decorator that measures the memory usage of a function.

    The ``Memory`` class is a subclass of the :class:`pydecorium.decorators.ProfilerUtils` base class.

    The ``data_name`` attribute is set to "memory usage".

    .. note::
    
        The memory handle result is given in bytes. It can be summed to get the total memory usage. The string_value method converts the result in bytes, kilobytes, megabytes.

    """
    data_name: str = "memory usage"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_execute(self, func, *args, **kwargs) -> None:
        """
        Computes the memory usage before the function execution.
        """
        self.process = psutil.Process()
        self.pre_execute_memory = self.process.memory_info().rss

    def post_execute(self, func, *args, **kwargs) -> None:
        """
        Computes the memory usage after the function execution.
        """
        self.post_execute_memory = self.process.memory_info().rss
    
    def handle_result(self) -> int:
        """
        Computes the memory usage.

        Returns
        -------
        int
            The memory usage in bytes.
        """
        return self.post_execute_memory - self.pre_execute_memory
    
    def string_value(self, result) -> str:
        """
        Converts the memory usage in bytes, kilobytes, megabytes in the format "{megabytes}MB {kilobytes}KB {bytes}B".
        
        Parameters
        ----------
        result: int
            The memory usage in bytes.

        Returns
        -------
        str
            The memory usage in bytes, kilobytes, megabytes.

        Raises
        ------
        TypeError
            If the parameter `result` is not an integer.
        """
        # Parameter check
        if not isinstance(result, int):
            raise TypeError("The parameter `result` must be an integer.")
        # Conversion
        megabytes, remainder = divmod(result, 1024**2)
        kilobytes, ubytes = divmod(remainder, 1024)
        return f"{megabytes}MB {kilobytes}KB {ubytes}B"




