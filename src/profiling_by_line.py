from line_profiler import LineProfiler
import inspect

def run_profiling_by_line(func, kwargs):
    line_profiler = LineProfiler()
    functions = inspect.getmembers(inspect.getmodule(func), inspect.isfunction)
    function_instances = dict(functions).values()

    for function_instance in function_instances:
        if function_instance is not func:
            line_profiler.add_function(function_instance)

    line_profiler_wrapper = line_profiler(func)
    line_profiler_wrapper(**kwargs)
    line_profiler.print_stats()

