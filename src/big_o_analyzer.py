from big_o import infer_big_o_class
import numpy as np

def extend_analyse(args, vals, plt):
    args_array = np.array(args)
    vals_array = np.array(vals)

    print("Big O analysis results:\n")
    best_fit, _ = infer_big_o_class(args_array, vals_array, verbose=True)
    best_fit = str(best_fit).replace("^", "**")
    print(f"\nBest fitted function:\n\n{best_fit}\n")

    best_fit_name = best_fit[:best_fit.find(':')]
    predicted_func_label = f"{best_fit_name} function"
    func_start = best_fit.find("time = ") + 7
    func_end = best_fit.find(" (sec)", func_start)
    function = best_fit[func_start:func_end]

    predicted_vals = []
    for n in args:
        predicted_vals.append(eval(function))

    plt.plot(args, predicted_vals, label=predicted_func_label)
