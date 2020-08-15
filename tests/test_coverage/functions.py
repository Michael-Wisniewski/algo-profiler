from math import floor

def get_floor(number):
    if isinstance(number, int):
        return number
    else:
        return apply_floor(number)

def apply_floor(number):
    return floor(number)
