from test_function import search
import random
import string
from src import Profiler

##### TEST DATA ############

test_set = [
    {
        "label": "List with wanted name.",
        "input": {
            "names": [
                "Paul",
                "Dennis",
                "Gregory",
                "Nathan",
                "Scott",
                "Julian",
                "Miles",
                "Laura",
            ],
            "wanted_name": "Scott",
        },
        "output": 4,
    },
    {
        "label": "List without wanted name.",
        "input": {
            "names": [
                "Paul",
                "Dennis",
                "Gregory",
                "Nathan",
                "Scott",
                "Julian",
                "Miles",
                "Laura",
            ],
            "wanted_name": "Steward",
        },
        "output": False,
    },
    {
        "label": "Test data with wrong anser.",
        "input": {
            "names": [
                "Paul",
                "Dennis",
                "Gregory",
            ],
            "wanted_name": "Steward",
        },
        "output": 1,
    },
]

##################################

##### TEST DATA GENERATOR #########


def data_gen_without_name(n):
    names = []
    letters = string.ascii_lowercase

    for _ in range(n):
        random_string = "".join(
            random.choice(letters) for i in range(random.randrange(5, 10))
        )
        names.append(random_string)

    return {"wanted_name": "Alan", "names": names}


def data_gen_with_name(n, name="John"):
    _, names = data_gen_without_name(n).values()
    random_index = random.randrange(n)
    names[random_index] = name
    return {"wanted_name": name, "names": names}


##################################

##### NAIVE ALGORITHM ############


def naive_search(wanted_name, names):
    return names.index(wanted_name) if wanted_name in names else False


##################################


profiler = Profiler()

profiler.run_tests(func=search, test_set=test_set)

profiler.run_stress_tests(
    func=search,
    naive_func=naive_search,
    data_gen=data_gen_with_name,
    gen_min_arg=1,
    gen_max_arg=1000,
    gen_steps=10,
)

profiler.run_coverage(func=search, test_set=test_set)

profiler.run_time_check(
    func=search,
    kwargs=data_gen_with_name(100)
)

profiler.run_timer(
    func=search,
    data_gen=data_gen_with_name,
    gen_min_arg=1000,
    gen_max_arg=10000,
    gen_steps=10,
    iterations=1,
)

profiler.run_c_profiler(
    func=search,
    kwargs=data_gen_with_name(10)
)

profiler.run_line_profiler(
    func=search,
    kwargs=data_gen_with_name(10)
)

profiler.run_memory_check(
    func=search,
    kwargs=data_gen_with_name(10)
)

profiler.run_memory_profiler(
    func=search,
    kwargs=data_gen_with_name(10)
)
