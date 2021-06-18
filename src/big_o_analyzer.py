from math import log, log2  # noqa

import numpy as np
from big_o import infer_big_o_class
from .helpers import LabelBase

from .big_o_complexities import ALL_CLASSES

class BigOLabels(LabelBase):
    RESULT = "Big O analysis results."
 
# ADD complexiteties here and remove .replace("^", "**").replace("x", "n")
# min 3 argumenty

def extend_analyse(args, vals, plt):
    args_array = np.array(args)
    vals_array = np.array(vals)

    print(f"{BigOLabels.RESULT}\n")
    best_fit, _ = infer_big_o_class(
        args_array, vals_array, verbose=True, classes=ALL_CLASSES
    )
    best_fit = str(best_fit).replace("^", "**").replace("x", "n")
    print(f"\nBest fitted function:\n\n{best_fit}\n")

    best_fit_name = best_fit[: best_fit.find(":")]
    predicted_func_label = f"{best_fit_name} function"
    func_start = best_fit.find("time = ") + 7
    func_end = best_fit.find(" (sec)", func_start)
    function = best_fit[func_start:func_end]

    predicted_vals = []
    for n in args:
        predicted_vals.append(eval(function))

    plt.plot(args, predicted_vals, label=predicted_func_label)
