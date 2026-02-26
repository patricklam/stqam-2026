def add_lists(list1, list2):
    """
    Requires: list1 and list2 are lists of ints
    Returns: a list containing the element-wise sum of the elements of list1 and list2
    Raises ValueError if list1 contains a negative integer.

    >>> add_lists([1, 2, 3], [6, 5, 4])
    [7, 7, 7]
    >>> add_lists([2, -1], [3, 5])
    Traceback (most recent call last):
      ...
    ValueError: negative value in list1 at position 1
    """
    r = []
    for i in range(0, len(list1)):
        if list1[i] < 0:
            raise ValueError(f"negative value in list1 at position {i}")
        r.append(list1[i] + list2[i])
    return r

if __name__ == "__main__":
    import doctest
    doctest.testmod()
