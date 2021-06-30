from setuptools import setup

long_description = """\
![lint](https://raw.githubusercontent.com/gist/Michael-Wisniewski/3f54787a495dfd8a05072c1eb12f9da3/raw/lint.svg)
![lines of code](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/gist/Michael-Wisniewski/3f54787a495dfd8a05072c1eb12f9da3/raw/lines_of_code.json)
![coverage](https://raw.githubusercontent.com/gist/Michael-Wisniewski/3f54787a495dfd8a05072c1eb12f9da3/raw/coverage.svg)
![python version](https://raw.githubusercontent.com/gist/Michael-Wisniewski/3f54787a495dfd8a05072c1eb12f9da3/raw/python_version.svg)

## algo-profiler

Package of profiling tools which allows to run function:
* unit tests
* stress tests
* coverage tests
* runtime check
* call time check
* call time check by line
* runtime analysis
* memory usage check
* memory usage check by line
* time based memory usage
* memory leaks check
* memory usage analysis
* comprehensive performance analysis
"""

setup(
    name="algo-profiler",
    version="0.0.24",
    description="A module for profiling algorithms.",
    author="Michał Wiśniewski",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://github.com/Michael-Wisniewski/algo-profiler",
    project_urls={
        "Documentation": "https://aroundpython.com/2021/06/13/tool-for-writing-algorithms/",
    },
    packages=["algo_profiler"],
    include_package_data=True,
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
    extras_require = {
        "dev": [
            "black",
            "check-manifest",
            "coverage-badge",
            "flake8",
            "isort",
            "parameterized",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-napoleon",
            "tox",
            "twine",
        ]
    },
    python_requires=">=3.8",
)
