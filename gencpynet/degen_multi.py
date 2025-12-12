# File: degen_multi.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2025
# License: GNU GPLv3
# Created On: 11 Dec 2025
# Purpose:
#   A Python translation of degen_multi.h and degen_multi.cc
# Notes:
#   Reconfigured the CPT to be a dictionary which takes a list of attribute values and produces a order list of results.
#   Attributes must go from 0 to (n-1)


#Returns true iff degenerate
#Note: This is not the most efficient approach, but should be adequate.
#
#Build CPT containing the assignments to parents as well as preference
#The resulting matrix is a truth table if d=2 and tables are complete
#

import itertools
import random


def match_except(lst1: list, lst2: list, idx: int) -> bool:
    """
    Returns true iff two lists are the same, except for at the provided index.
    :param lst1: A list of items to compare.
    :param lst2: A list of items to compare.
    :param idx: The index to ignore.
    :return: true iff the two lists are the same except at the given index.
    """
    return lst1[:idx] == lst2[:idx] and lst1[idx+1:] == lst2[idx+1:]

def degen_multi(cpt: dict[list[int], list[int]], indegree: int, dom_size: int) -> bool:
    """
    Determines if a provided cpt is degenerate.
    :param cpt: A dictionary which takes list of parent values (order is assumed to be based on common ordering)
        and maps it to a ordering of the values for the associated attribute.
    :param indegree: The number of parents of the attribute whose cpt is being tested.
    :param dom_size: The size of an attribute's domain (homogeneous domains.)
    :return: True iff the cpt in question is degenerate.
    """
    # For each attribute determine if the given cpt depends on it.
    for attr in range(indegree):
        # Test all pairs of values
        for val1 in range(dom_size):
            for val2 in range(val1+1, dom_size):
                val1_rows = []
                val2_rows = []
                # Extract pertinent rows
                for key in cpt.keys():
                    if key[attr] == val1:
                        val1_rows.append(key)
                    elif key[attr] == val2:
                        val2_rows.append(key)
                # Find rows which are the same except for the attr under consideration
                dependent = False
                for v1_row in val1_rows:
                    for v2_row in val2_rows:
                        if match_except(v1_row, v2_row, attr):
                            # Determine if they are the same or not. If not then we have dependency.
                            if cpt[v1_row] != cpt[v2_row]:
                                dependent = True
                            break
                    if dependent:
                        break
                # Once we find a lack of dependence once, we know it is degenerate.
                if not dependent:
                    return True
    return False

# Generate a random, non-degenerate cpt (multi, incomplete)
def rand_cpt(indegree: int, dom_size: int, iChance: float) -> dict[list[int], list[int]]:
    cpt = None
    # Generate all the possible combinations of values which might act as keys.
    dom_vals = [i for i in range(dom_size)]
    all_rows = itertools.product(dom_vals, repeat=indegree)
    # Lack of a do while requires this construction.
    while cpt is None or degen_multi(cpt, indegree, dom_size):
        if cpt is None:
            cpt = dict()
        for row in all_rows:
            if random.uniform(0.0, 1.0) >= iChance:
                order = dom_vals[:]
                random.shuffle(order)
                cpt[list(row)] = order
    return cpt
