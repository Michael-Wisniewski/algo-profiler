def sort(A, n, m):
    """Time complexity: Θ(n) if m is constant, memory consumption - Θ(n).

    >>> numbers = [1, 0, 4, 2, 3, 0, 2, 0, 1]
    >>> numbers_count = 9
    >>> max_number = 4
    >>> sort(numbers, numbers_count, max_number)
    [0, 0, 0, 1, 1, 2, 2, 3, 4]
    """

    equal_keys = count_equal_keys(A, n, m)
    smaller_keys = count_smaller_keys(equal_keys, m)
    return reorganize(A, smaller_keys, n, m)


def reorganize(A, smaller_keys, n, m):
    """Time complexity: Θ(n) if m is constant, memory consumption - Θ(n).

    >>> numbers = [1, 0, 4, 2, 3, 0, 2, 0, 1]
    >>> numbers_count = 9
    >>> max_number = 4
    >>> equal_keys = count_equal_keys(numbers, numbers_count, max_number)
    >>> smaller_keys = count_smaller_keys(equal_keys, max_number)
    >>> reorganize(numbers, smaller_keys, numbers_count, max_number)
    [0, 0, 0, 1, 1, 2, 2, 3, 4]
    """

    B = [0] * n
    subsequent = [0] * (m + 1)

    for j in range(0, m + 1):
        subsequent[j] = smaller_keys[j] + 1

    for i in range(0, n):
        key = A[i]
        index = subsequent[key]
        B[index - 1] = A[i]
        subsequent[key] += 1

    return B


def count_smaller_keys(equal_keys, m):
    """Time complexity: Θ(n), memory consumption - Θ(n).

    >>> numbers = [1, 0, 4, 2, 3, 0, 2, 0, 1]
    >>> numbers_count = 9
    >>> max_number = 4
    >>> equal_keys = count_equal_keys(numbers, numbers_count, max_number)
    >>> count_smaller_keys(equal_keys, max_number)
    [0, 3, 5, 7, 8]
    """

    smaller_keys = [0] * (m + 1)

    for i in range(1, (m + 1)):
        smaller_keys[i] = smaller_keys[i - 1] + equal_keys[i - 1]

    return smaller_keys


def count_equal_keys(A, n, m):
    """Time complexity: Θ(n) if m is constant, memory consumption - Θ(n).

    >>> numbers = [1, 0, 4, 2, 3, 0, 2, 0, 1]
    >>> numbers_count = 9
    >>> max_number = 4
    >>> count_equal_keys(numbers, numbers_count, max_number)
    [3, 2, 2, 1, 1]
    """

    equal_keys = [0] * (m + 1)
    
    for i in range(0, n):
        index = A[i]
        equal_keys[index] += 1

    return equal_keys
