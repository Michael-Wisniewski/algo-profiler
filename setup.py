from setuptools import setup

setup(
    name="algo-profiler",
    version="0.0.1",
    description="A module for profiling algorithms.",
    author="Michał Wiśniewski",
    py_modules=["Profiler"],
    package_dir={"": "src"},
    install_requires=[
        "big_o",
        "coverage",
        "line_profiler",
        "matplotlib",
        "memory_profiler",
        "objsize",
        "pympler",
        "scalene",
        "snakeviz",
    ],
    extra_require = {
        "dev": [
            "black",
            "flake8",
            "isort",
            "parameterized",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-napoleon",
        ]
    }
)
