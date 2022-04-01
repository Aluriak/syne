


def right_left_walk(size:int) -> [int]:
    """Yield index of objects to visit for a right left walk

    >>> tuple(right_left_walk(5))
    (2, 3, 1, 4, 0)

    """
    middle = size // 2
    yield middle
    low, up = middle-1, middle+1
    change = True
    while change:
        change = False
        if up < size:
            yield up
            up += 1
            change = True
        if low >= 0:
            yield low
            low -= 1
            change = True


