# File: utils.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2025
# License: GNU GPLv3
# Created On: 11 Dec 2025
# Purpose:
#   Various utility functions for generating CP-nets
# Notes:

import random

# Knuth's algorithm 3.4.2S: Select a subset of size n from a set of size N.
# Translator's note: Original relied on specifics of a bit string, converted to be more Pythonic
def random_k_subset(set_size: int, subset_size: int) -> list[int]:
    """
    An implementation of Knuth's algorithm 3.4.2S
    :param set_size: The number of items in the set you are sampling from.
    :param subset_size: The size of the subset to return.
    :return: Returns a list of the numbers between 0 and set_size-1 which were selected.
    """
    result = []
    traversed = 0
    selected = 0
    for idx in range(set_size):
        decider = random.uniform(0, 1.0)
        if ((set_size - traversed) * decider) < (subset_size - selected):
            result.append(idx)
            selected += 1
        traversed += 1
        # If done early break
        if selected == subset_size:
            break
    return result