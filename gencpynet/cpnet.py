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
        self.__table: None | dict[str | tuple[int,...], tuple[int,...]] = None
        if indegree == 0:
            self.__table = dict()
            order = domain.feature_values()
            random.shuffle(order)
            self.__table['default'] = tuple(order)
        else:
            while self.__table is None or self.__is_degen():
                self.__table = dict()
                all_rows = itertools.product(domain.feature_values(), repeat=indegree)
                for row in all_rows:
                    if random.uniform(0.0, 1.0) >= incomp_chance:
                        order = domain.feature_values()
                        random.shuffle(order)
                        self.__table[row] = tuple(order)

    def get_order(self, alt_project: tuple[int,...]) -> tuple[int,...] | None:
        """
        Gets the preference order given a projected alternative (only containing pertinent attrs, in proper order) for
        the CPTs attribute.
        :param alt_project: A tuple of integer values indicating the required attribute values to make an order
            determination. If len(alt_project) is 0 then the default is returned.
        :return: The ordered list of values for the attr the CPT represents. If None is returned then a CPT row does
            not exist, likely due to incompleteness.
        """
        if len(alt_project) == 0:
            return self.__table['default']
        elif alt_project in self.__table:
            return self.__table[alt_project]
        return None

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
                        if CPT.matching_except(top_row, row, attr):
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
    def matching_except(lst1: list | tuple, lst2: list | tuple, idx: int) -> bool:
        """
        Returns true iff two lists are the same, except for at the provided index.
        :param lst1: A list of items to compare.
        :param lst2: A list of items to compare.
        :param idx: The index to ignore.
        :return: true iff the two lists are the same except at the given index.
        """
        return lst1[:idx] == lst2[:idx] and lst1[idx+1:] == lst2[idx+1:]


class CPNode:
    def __init__(self, attr: int, parents: list[int], incomp_chance: float, domain: Domain):
        """
        Constructor for the CPNode class. Generates a random CPT for the node as well.
        :param attr: The attribute the node is associated with.
        :param parents: The list of parents of the node.
        :param incomp_chance: The chance that a row is missing from the CPT.
        :param domain: The domain of valid alternatives.
        """
        self.__attr = attr
        self.__parents = parents
        self.__domain = domain
        self.__cpt = CPT(len(parents), incomp_chance, domain)

    def dominates(self, alt1: Alternative, alt2: Alternative) -> bool | None:
        """
        Determines if alt1 dominates alt2. Only works if alt1 and alt2 only differ on the node's attribute.
        :param alt1: A valid alternative.
        :param alt2: A valid alternative.
        :return: True if alt1 > alt2, false if alt1 <= alt2. Returns None if alt1 >< alt2.
        """
        if not CPT.matching_except(alt1.as_tuple(), alt2.as_tuple(), self.__attr):
            raise ValueError("Cannot compare two alternatives at a node if they differ in > 1 attribute.")
        cpt_proj = alt1.project(self.__parents)
        order = self.__cpt.get_order(cpt_proj)
        if order is None:
            return None
        return order.index(alt1[self.__attr]) < order.index(alt2[self.__attr])

    def worsening_flips(self, alt: Alternative) -> tuple[int,...]:
        """
        Finds all worsening flip values for the given alternative at the given node.
        :param alt: A valid alternative.
        :return: A list of all worsening flip values according to the node. May return empty list.
        """
        cpt_proj = alt.project(self.__parents)
        order = self.__cpt.get_order(cpt_proj)
        if order is None:
            return tuple()
        return order[order.index(alt[self.__attr])+1:]