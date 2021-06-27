from test_function import increment_by_one
from src import Profiler


test_set = [
    {
        "label": "Empty list",
        "input": {
            "numbers_list": [],
        },
        "output": [],
    },
    {
        "label": "List with positive numbers.",
        "input": {
            "numbers_list": [1, 5, 7],
        },
        "output": [2, 6, 8],
    },
    {
        "label": "List with negative numbers.",
        "input": {
            "numbers_list": [-2, -7, -3],
        },
        "output": [-1, -6, -2],
    },
     {
        "label": "List with large numbers.",
        "input": {
            "numbers_list": [100000000, 9999999999999999999],
        },
        "output": [100000001, 10000000000000000000],
    },
]

def data_gen(list_length):
    """
    >>> data_gen(3)
    {'numbers_list': [0, 1, 2]}

    >>> data_gen(7)
    {'numbers_list': [0, 1, 2, 3, 4, 5, 6]}
    """

    numbers_list = [number for number in range(list_length)]
    return {"numbers_list" : numbers_list}

def naive_increment_by_one(numbers_list):
    return [number + 1 for number in numbers_list]


profiler = Profiler()

# profiler.run_tests(func=increment_by_one, test_set=test_set)

# profiler.run_stress_tests(
#     func=increment_by_one,
#     naive_func=naive_increment_by_one,
#     data_gen=data_gen,
#     gen_min_arg=1,
#     gen_max_arg=100,
#     gen_steps=10,
# )

# profiler.run_coverage(func=increment_by_one, test_set=test_set)

# profiler.run_time_check(
#     func=increment_by_one,
#     kwargs=data_gen(10000000),
#     iterations=10
# )

# profiler.run_cProfile(
#     func=increment_by_one,
#     kwargs=data_gen(10000000)
# )

# profiler.run_snakeviz(
#     func=increment_by_one,
#     kwargs=data_gen(10000000)
# )

# profiler.run_line_profiler(
#     func=increment_by_one,
#     kwargs=data_gen(10000000)
# )

# profiler.run_time_analysis(
#     func=increment_by_one,
#     data_gen=data_gen,
#     gen_min_arg=10,
#     gen_max_arg=1000000,
#     gen_steps=10,
#     find_big_o=True
# )

# profiler.run_memory_check(
#     func=increment_by_one,
#     kwargs=data_gen(10000000)
# )

# profiler.run_memory_profiler(
#     func=increment_by_one,
#     kwargs=data_gen(1000000),
#     clean_result=True
# )

# profiler.run_time_based_memory_usage(
#     func=increment_by_one,
#     kwargs=data_gen(10000000)
# )

# profiler.run_check_memory_leaks(
#     func=increment_by_one,
#     kwargs=data_gen(100000)
# )

profiler.run_memory_analysis(
    func=increment_by_one,
    data_gen=data_gen,
    gen_min_arg=100,
    gen_max_arg=1000,
    gen_steps=10,
    find_big_o=True
)

# profiler.run_scalene(
#     func=increment_by_one,
#     kwargs=data_gen(1000000),
#     cpu_sampling_rate=0.001
# )
