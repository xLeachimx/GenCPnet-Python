# File: cpnet.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2025
# License: GNU GPLv3
# Created On: 11 Dec 2025
# Purpose:
#   A series of classes for handling CP-nets.
# Notes:

from alternative import Alternative, Domain
import itertools
import random

class CPT:
    """Class for generating/dealing with a Conditional Preference Table."""
    def __init__(self, indegree: int, incomp_chance: float, domain: Domain):
        """
        Creates a random new CPT with the given parameters.
        :param indegree: The indegree of the node associated with this CPT.
        :param incomp_chance: The chance of a row in the CPT being empty.
        :param domain: The domain of the CPT.
        """
        self.__indegree = indegree
        self.__incomp_chance = incomp_chance
        self.__domain = domain
        self.__table = None
        while self.__table is None or self.__is_degen():
            self.__table = dict()
            all_rows = itertools.product(domain.feature_values(), repeat=indegree)
            for row in all_rows:
                if random.uniform(0.0, 1.0) >= incomp_chance:
                    order = domain.feature_values()
                    random.shuffle(order)
                    self.__table[row] = order

    def __is_degen(self):
        """
        Determines if a CPT is degenerate.
        :return: True iff the cpt in question is degenerate.
        """
        # For each attribute determine if the given CPT depends on it.
        for attr in range(self.__indegree):
            # Test that rows preference order change with the value of the attr.
            # Translator's note: This might actually be a big bug in the original for feature domains > 2.
            val_rows = [[] for i in range(self.__domain.feature_domain_size())]
            # Extract and bucket rows based on attribute values
            for key in self.__table.keys():
                val_rows[key[attr]] = key
            dependent = False
            for top_row in val_rows[0]:
                matching_rows = []
                # Find rows with identical settings (except the attr in question.)
                for idx in range(1, len(val_rows)):
                    for row in val_rows[idx]:
                        if CPT.__matching_except(top_row, row, attr):
                            matching_rows.append(row)
                # For those matching rows see if anything changes, if so then dependency exists.
                for row in matching_rows:
                    if self.__table[top_row] != self.__table[row]:
                        dependent = True
                        break
                if dependent:
                    break
            if not dependent:
                return False
        return True

    @staticmethod
    def __matching_except(lst1: list, lst2: list, idx: int) -> bool:
        """
        Returns true iff two lists are the same, except for at the provided index.
        :param lst1: A list of items to compare.
        :param lst2: A list of items to compare.
        :param idx: The index to ignore.
        :return: true iff the two lists are the same except at the given index.
        """
        return lst1[:idx] == lst2[:idx] and lst1[idx+1:] == lst2[idx+1:]


def degen_multi(cpt: dict[list[int], list[int]], indegree: int, dom_size: int) -> bool:

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
