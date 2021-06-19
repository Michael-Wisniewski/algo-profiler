from math import floor

def get_floor2(number):
    if isinstance(number, int):
        return number
    else:
        return apply_floor2(number)

def apply_floor2(number):
    return floor(number)
