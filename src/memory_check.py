import inspect

from memory_profiler import LineProfiler, show_results


class MemoryCheck:
    def __init__(self):
        self.helper_funcs = {}

    def get_mem_usage(self, func, kwargs):
        profiler = LineProfiler()
        profiler(func)(**kwargs)
        usage_by_lines = list(profiler.code_map.values())[0]
        usage_on_start = list(usage_by_lines.values())[0][1]
        usage_on_end = list(usage_by_lines.values())[-1][1]
        return usage_on_end - usage_on_start

    def get_args_decorator(self, func):
        def wrapper(*args, **kwargs):
            self.helper_funcs[func.__name__]["call_params"].append(
                {"args": args, "kwargs": kwargs}
            )
            return func(*args, **kwargs)

        return wrapper

    def clean_result(self, profiler):
        code_map = profiler.code_map
        usage_by_lines = list(code_map.values())[0]
        initial_usage = list(usage_by_lines.values())[0][1]

        for code_obj_key, code_lines in dict(code_map).items():
            first_line_usage_key = list(code_map[code_obj_key].keys())[0]
            _, usage, occurences = code_map[code_obj_key][first_line_usage_key]
            code_map[code_obj_key][first_line_usage_key] = (0.0, usage, occurences)

            for line_key, line_usage in code_lines.items():
                increment, usage, occurences = line_usage
                usage -= initial_usage
                code_map[code_obj_key][line_key] = (increment, usage, occurences)

    def run_memory_check(self, func, kwargs):
        self.helper_funcs = {}
        func_module = inspect.getmodule(func)
        funcs = inspect.getmembers(func_module, inspect.isfunction)
        
        profiler = LineProfiler()
        wrapper = profiler(func)

        for func_name, func_instance in funcs:
            if func_name == func.__name__:
                continue

            profiler.code_map.add(func_instance.__code__)
        
        wrapper(**kwargs)
        self.clean_result(profiler)
        show_results(profiler)
