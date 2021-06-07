from argparse import Namespace
import inspect
from scalene.scalene_profiler import Scalene
import os
from textwrap import dedent
import sys

def scalene_analyzer(func, kwargs, interval=float("inf")):
        scalene_triger = dedent(f"""\
        if __name__ == "__main__":
            kwargs = {kwargs}
            {func.__name__}(**kwargs)    
         """)

        input_path = os.path.abspath(inspect.getfile(func))
        output_path = os.path.join(
            os.path.dirname(__file__), "temp_files", "scalene_temp.py"
        )

        with open(output_path, "w") as output_file:
            with open(input_path, "r") as input_file:
                output_file.write(input_file.read())

            output_file.write(scalene_triger)

        args = Namespace(
            cpu_only=False,
            cpu_percent_threshold=1,
            cpu_sampling_rate=0.001,
            malloc_threshold=10,
            outfile=None,
            profile_all=True,
            profile_interval=interval,
            reduced_profile=False,
            use_virtual_time=False,
        )

        # sys.argv.append("cpu_percent_threshold=0.001")
        sys.argv.append(output_path)
        Scalene.main()
        # os.remove(output_path)


        scalene --cpu-percent-threshold 1 --cpu-sampling-rate 0.0001 ./src/temp_files/scalene_temp.py
