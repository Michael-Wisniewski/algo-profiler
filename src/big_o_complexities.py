import numpy as np
from big_o.complexities import ComplexityClass


class Constant(ComplexityClass):
    order = 10

    def _transform_n(self, n):
        return np.ones((len(n), 1))

    @classmethod
    def format_str(cls):
        return "time = {:.2G}"


class Linear(ComplexityClass):
    order = 30

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*n"


class Quadratic(ComplexityClass):
    order = 50

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * n]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*n^2"


class Cubic(ComplexityClass):
    order = 60

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n ** 3]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*n^3"


class BinaryLogarithmic(ComplexityClass):
    order = 20

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log2(n)]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*log2(n)"


class Logarithmic(ComplexityClass):
    order = 25

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*log(n)"


class BinaryLinearithmic(ComplexityClass):
    order = 40

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log2(n)]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*n*log2(n)"


class Linearithmic(ComplexityClass):
    order = 45

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    @classmethod
    def format_str(cls):
        return "time = {:.2G} + {:.2G}*n*log(n)"


class Polynomial(ComplexityClass):
    order = 70

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return "time = {:.2G} * n^{:.2G}"


class Exponential(ComplexityClass):
    order = 80

    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def _transform_time(self, t):
        return np.log(t)

    @classmethod
    def format_str(cls):
        return "time = {:.2G} * {:.2G}^n"


ALL_CLASSES = [
    Constant,
    Linear,
    Quadratic,
    Cubic,
    Polynomial,
    BinaryLogarithmic,
    Logarithmic,
    BinaryLinearithmic,
    Linearithmic,
    Exponential,
]
