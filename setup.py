from setuptools import setup

setup(
    name="algo-profiler",
    version="0.0.1",
    description="A module for profiling algorithms.",
    author="Michał Wiśniewski",
    py_modules=["Profiler"],
    package_dir={"": "src"},
    install_requires=[
       "line-profiler==3.0.2",
        "memory-profiler==0.54.0"
    ],
    extra_require = {
        "dev": [
            "black==21.4b2",
            "parameterized==0.8.1",
            "coverage==5.5"
        ]
    }
)
