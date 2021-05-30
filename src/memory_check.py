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
        func_names = list(dict(funcs).keys())
        func_names.remove(func.__name__)

        for func_name in func_names:
            func_instance = getattr(func_module, func_name)
            setattr(func_module, func_name, self.get_args_decorator(func_instance))
            self.helper_funcs[func_name] = {
                "instance": func_instance,
                "call_params": [],
            }

        profiler = LineProfiler()
        profiler(func)(**kwargs)
        self.clean_result(profiler)
        show_results(profiler)

        for helper_func in self.helper_funcs.values():
            if not helper_func["call_params"]:
                continue

            profiler = LineProfiler()
            wrapper = profiler(helper_func["instance"])

            for params in helper_func["call_params"]:
                wrapper(*params["args"], **params["kwargs"])

            self.clean_result(profiler)
            show_results(profiler)
