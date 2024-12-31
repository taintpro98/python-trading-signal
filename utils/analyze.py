from typing import List

def find_bottoms(data: List[float]) -> List[int]:
    """
    Finds the indices of the bottoms in a float array.
    A bottom is a point smaller than its immediate neighbors.

    :param data: List[float] - Array of float values to search for bottoms.
    :return: List[int] - List of indices representing the bottoms.
    """
    if len(data) < 3:
        # There can't be any bottoms in arrays shorter than 3
        return []

    bottoms = []
    for i in range(1, len(data) - 1):
        if data[i] < data[i - 1] and data[i] < data[i + 1]:
            bottoms.append(i)
    return bottoms