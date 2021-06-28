from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="algo-profiler",
    version="0.0.2",
    description="A module for profiling algorithms.",
    author="Michał Wiśniewski",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://github.com/Michael-Wisniewski/algo-profiler",
    packages=["algo_profiler"],
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
            "flake8",
            "isort",
            "parameterized",
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-napoleon",
            "tox",
            "twine",
        ]
    }
)
