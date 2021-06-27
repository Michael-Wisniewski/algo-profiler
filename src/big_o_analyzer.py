from math import log, log2  # noqa

import numpy as np
from big_o import infer_big_o_class

from .big_o_complexities import ALL_CLASSES
from .helpers import LabelBase


class BigOLabels(LabelBase):
    RESULT = "Big O analysis results."
    BEST_FIT = "Best fitted function"
    NOT_ENOUGH_POINTS = "There must be at least three points to make an analysis."
    TOO_BIG_ARGS = "Warning - The n was too big and was scaled down to range <0, 100000>."
    TOO_SMALL_VALS = "Warning - The measured values were too small and were normalized."


def extend_analyse(args, vals, plt=None):

    print('args', args)
    print('vals', vals)
    if len(args) < 3:
        raise ValueError(BigOLabels.NOT_ENOUGH_POINTS)

    # Scale down n to range <0, 10000> if necessary.
    args_array = np.array(args)
    args_scale_factor = 1 

    if np.max(args_array) > 100000:
        args_scale_factor = 100000 / np.max(args_array)
        print(BigOLabels.TOO_BIG_ARGS, end='\n\n')

    args_array = args_array * args_scale_factor

    # Normalize vals is necessary.
    vals_array = np.array(vals)
    vals_mean = 0
    vals_std = 1

    if np.max(vals_array) < 0.001:
        vals_mean = np.mean(vals)
        vals_std = np.std(vals)
        print(BigOLabels.TOO_SMALL_VALS, end='\n\n')

    vals_array = (vals_array - vals_mean) / vals_std

    print(f"{BigOLabels.RESULT}\n")
    best_fit, _ = infer_big_o_class(
        args_array, vals_array, verbose=True, classes=ALL_CLASSES
    )
    best_fit = str(best_fit).replace("^", "**")
    print(f"\n{BigOLabels.BEST_FIT}:\n\n{best_fit}\n")

    best_fit_name = best_fit[: best_fit.find(":")]
    predicted_func_label = f"{best_fit_name} function"
    func_start = best_fit.find("time = ") + 7
    func_end = best_fit.find(" (sec)", func_start)
    function = best_fit[func_start:func_end]

    if plt is not None:
        predicted_vals = []
        
        for n in args:
            n = n * args_scale_factor
            denormalized_prediction = eval(function) * vals_std + vals_mean
            predicted_vals.append(denormalized_prediction)

        plt.plot(args, predicted_vals, label=predicted_func_label)
