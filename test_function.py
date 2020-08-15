def search(wanted_name, names):
    if len(names) == 0:
        return False

    name_index = False
    
    for index, name in enumerate(names):
        if name == wanted_name:
            name_index = index

    [1] * 10 ** 7 # creating list for slowing down code
    
    return name_index
