import inspect
import os
import pickle
import sys
from textwrap import dedent

from scalene.scalene_profiler import Scalene


def scalene_analyzer(func, kwargs={}, cpu_sampling_rate=0.1):
    input_path = os.path.abspath(inspect.getfile(func))
    output_path = os.path.join(
        os.path.dirname(__file__), "temp_files", "scalene_temp.py"
    )
    kwargs_path = os.path.join(
        os.path.dirname(__file__), "temp_files", "kwargs_temp.pickle"
    )

    scalene_triger = dedent(
        f"""\
    if __name__ == "__main__":
        import pickle
        with open("{kwargs_path}", "rb") as kwargs_file:
            kwargs = pickle.load(kwargs_file)
        {func.__name__}(**kwargs)
    """
    )

    with open(output_path, "w") as output_file:
        with open(input_path, "r") as input_file:
            output_file.write(input_file.read())

        output_file.write(scalene_triger)

    with open(kwargs_path, "wb") as kwargs_file:
        pickle.dump(kwargs, kwargs_file)

    args = [
        "--cpu-percent-threshold",
        "1",
        "--cpu-sampling-rate",
        str(cpu_sampling_rate),
        "--malloc-threshold",
        "10",
        "--profile-interval",
        "inf",
    ]

    sys.argv = args
    sys.argv.append(output_path)

    try:
        Scalene.main()
    except SystemExit as system_exit:
        if system_exit.code ==0:
            pass
    finally:
        os.remove(output_path)
        os.remove(kwargs_path)
