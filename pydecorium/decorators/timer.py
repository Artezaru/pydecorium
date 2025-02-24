from .profiler_utils import ProfilerUtils
import time

class Timer(ProfilerUtils):
    """
    ``Timer`` class is a decorator that measures the runtime of a function.

    The ``Timer`` class is a sub-class of the :class:`pydecorium.decorators.ProfilerUtils` base class.

    The ``data_name`` attribute is set to "runtime".

    .. note::
    
        The runtime handle result is given in seconds. It can be summed to get the total runtime. The string_value method converts the result in hours, minutes and seconds.
    """
    data_name: str = "runtime"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_execute(self, func, *args, **kwargs) -> None:
        """
        Initializes the timer before the function execution.
        """
        self.tic = time.time()

    def post_execute(self, func, *args, **kwargs) -> None:
        """
        Computes the runtime after the function execution.
        """
        self.toc = time.time()
    
    def handle_result(self) -> float:
        """
        Computes the runtime.

        Returns
        -------
        float
            The runtime in seconds.
        """
        return self.toc - self.tic
    
    def string_value(self, result) -> str:
        """
        Converts the runtime in hours, minutes and seconds in the format "{hours}h {minutes}m {seconds}s".

        Parameters
        ----------
        result : float
            The runtime in seconds.

        Returns
        -------
        str
            The runtime in hours, minutes and seconds.

        Raises
        ------
        TypeError
            If `result` is not a numeric.
        """
        # Parameter check
        if not isinstance(result, (float, int)):
            raise TypeError("The parameter `result` must be numeric.")
        # Conversion
        hours, remainder = divmod(result, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {seconds:.4f}s"



