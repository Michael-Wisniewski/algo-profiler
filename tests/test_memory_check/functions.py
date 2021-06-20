from math import floor

def create_list(n):
    return [1] * 10 ** 5 * n

def get_floor(number):
    if isinstance(number, int):
        return number
    else:
        return apply_floor(number)

def apply_floor(number):
    return floor(number)
