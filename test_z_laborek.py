from func import sort_by_counting_equal_keys as func
from src import Profiler
from random import randrange

profiler = Profiler()

def data_gen(n):
    result = []

    for i in range(n, 0, -1):
       result.append(randrange(0, 4))

    return {'A': result, 'n': n, 'm': 4}





profiler.run_time_analysis(
    func=func,
    data_gen=data_gen,
    gen_min_arg=100,
    gen_max_arg=1000000,
    gen_steps=10,
    iterations=1,
    draw_chart=True,
    find_big_o=True
)



# profiler.run_memory_analysis(
#     func=func,
#     data_gen=data_gen,
#     gen_min_arg=100,
#     gen_max_arg=100000,
#     gen_steps=10,
#     draw_chart=True,
#     find_big_o=True
# )

# profiler.run_scalene(
#     func=func,
#     kwargs=data_gen(10000),
#     cpu_sampling_rate=0.001
# )

# profiler.run_memory_profiler(
#     func=func,
#     kwargs=data_gen(100000)
# )

# profiler.run_scalene(
#     func=func1,
#     kwargs=data_gen(2900),
#     cpu_sampling_rate=0.001
# )

# profiler.run_scalene(
#     func=func,
#     kwargs=data_gen(2900),
#     cpu_sampling_rate=0.001
# )

# profiler.run_scalene(
#     func=func,
#     kwargs=data_gen(2000)
# )



# profiler.run_time_check(
#     func=func1,
#     kwargs=data_gen(2900),
#     iterations=1000
# )

# profiler.run_time_check(
#     func=func,
#     kwargs=data_gen(1000),
#     iterations=1000
# )




# profiler.run_scalene(
#     func=func,
#     kwargs=data_gen(1000),
#     cpu_sampling_rate=0.001
# )

# profiler.run_memory_analysis(
#     func=func2,
#     data_gen=data_gen,
#     gen_min_arg=10,
#     gen_max_arg=30330,
#     gen_steps=100,
#     draw_chart=True,
#     find_big_o=True
# )

# # Stałe zużycie pamięci w czasie.
# profiler.run_time_based_memory_usage(
#     func=func,
#     kwargs=data_gen(1000000),
#     interval=0.0001
# )

# profiler.run_scalene(
#     func=search,
#     kwargs=data_gen(1000000),
#     cpu_sampling_rate=0.001
# )

# profiler.run_memory_analysis(
#     draw_chart=True,
#     func=search,
#     data_gen=data_gen,
#     gen_min_arg=1000,
#     gen_max_arg=100000,
#     gen_steps=5,
#     find_big_o=True
# )


  