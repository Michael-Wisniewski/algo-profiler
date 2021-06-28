def linear_space(min_val, max_val, steps_num):
    for value in [min_val, max_val, steps_num]:
        if not isinstance(value, int) or value < 0:
            raise TypeError("All arguments have to be positive integers.")

    if max_val < min_val:
        raise ValueError("Maximal argument can not be smaller than minimal.")

    total_digits_num = max_val - min_val + 1

    if steps_num > total_digits_num:
        steps_num = total_digits_num
        print(
            "Warning: number of steps was reduced to maximum available value "
            f"for range <{min_val},{max_val}> to {total_digits_num}."
        )

    if steps_num == 1:
        return [min_val]

    step = ((total_digits_num - steps_num) // (steps_num - 1)) + 1
    return [min_val + (step * index) for index in range(steps_num)]
