# File: alternative.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2025
# License: GNU GPLv3
# Created On: 11 Dec 2025
# Purpose:
#   A class to handle alternatives in a manner which will make using the generated CP-nets easier.
# Notes:
#   Provides a class for alternatives and well as homogenous preference domains.
from typing import Iterator
from utils import random_k_subset
import random


class Alternative:
    def __init__(self, values: list[int]):
        """
        Constructor for the Alternative class.
        :param values: A list representing the values of features (using integers only.)
        """
        self.__feature_values = values[:]

    def length(self) -> int:
        """
        Gets the length of the alternative.
        :return: The length of the alternative.
        """
        return len(self.__feature_values)

    def project(self, indices: list[int]) -> tuple[int,...]:
        """
        Returns the projection of the alternative to the given indices (in that order.)
        :param indices: An order list of indices to project the alternative onto.
        :return: A tuple of integers representing the projection of the alternative.
        """
        return tuple(self.__feature_values[idx] for idx in indices)

    def as_tuple(self) -> tuple[int,...]:
        return tuple(self.__feature_values)

    def __getitem__(self, idx: int | list[int]) -> int | tuple[int,...]:
        """
        Gets either one value or a list of values based on the indices given.
        :param idx: An integer or list of integers indicating the features to extract.
        :return:
        """
        if isinstance(idx, int):
            return self.__feature_values[idx]
        elif isinstance(idx, list) and isinstance(idx[0], int):
            return self.project(idx)
        raise IndexError(f"Cannot project alternative onto {type(idx)} type object.")

    def __len__(self) -> int:
        """
        Gets the length of the alternative.
        :return: The length of the alternative.
        """
        return self.length()

    def __eq__(self, other: 'Alternative') -> bool:
        """
        Determines equivalence between alternatives.
        :param other: Another valid Alternative object.
        :return: True if the alternatives are identical, including size.
        """
        if len(self) != len(other):
            return False
        return self.__feature_values == other.__feature_values

class Domain:
    def __init__(self, features: int, dom_size: int):
        """
        Constructor for the Domain class.
        :param features: The number of features in the domain.
        :param dom_size: The size of the feature domains in the domain.
        """
        self.__features = features
        self.__dom_size = dom_size

    def size(self) -> int:
        """
        Computes the total size of the domain.
        :return: The number of alternatives contained in the domain.
        """
        return self.__dom_size ** self.__features

    def is_member(self, alt: Alternative) -> bool:
        """
        Returns true if the alternative could be a member of the current domain.
        :param alt: A valid Alternative object.
        :return: True if the provided alternative could be in the Domain, false otherwise.
        """
        if len(alt) != self.__features:
            return False
        for idx in range(len(alt)):
            if alt[idx] >= self.__dom_size:
                return False
        return True

    def each_alternative(self, start: None | Alternative) -> Iterator[Alternative]:
        """
        An iterator function for iterating through each alternative in the domain.
        :param start: The alternative to start with. Excludes start. If None all alternatives generated. (default: None)
        :return: Yields each alternative one at a time.
        """
        if start is None:
            start = [0 for _ in range(self.__features)]
            yield Alternative(start)
        else:
            if self.is_member(start):
                start = list(start.as_tuple())
            else:
                start = [0 for _ in range(self.__features)]
                yield Alternative(start)
        while sum(start) != (self.__features * self.__dom_size):
            for idx in range(len(start)):
                start[idx] += 1
                if start[idx] >= self.__dom_size:
                    start[idx] = 0
                else:
                    break
            yield Alternative(start)

    def each_pair(self) -> Iterator[tuple[Alternative, Alternative]]:
        """
        An iterator function for iterating through all unique pairs of alternatives in the domain.
        :return: Yields each unique pair of alternatives one at a time.
        """
        for alt1 in self.each_alternative():
            for alt2 in self.each_alternative(alt1):
                yield alt1, alt2

    def generate_alternative(self) -> Alternative:
        """
        Generates a random alternative from the domain.
        :return: An Alternative object which is a member of the domain.
        """
        return Alternative([random.randrange(self.__dom_size) for _ in range(self.__features)])

    def generate_pair(self, hamming_distance: int = 0) -> tuple[Alternative, Alternative]:
        """
        Creates a random pair of alternatives with the given hamming distance.
        :param hamming_distance: The hamming distance of the alternatives. If hamming_distance is <= 0, then no
            consideration of hamming distance is done. (default: 0)
        :return: A pair of alternatives with the given hamming distance.
        """
        alt1 = self.generate_alternative()
        alt2 = self.generate_alternative()
        if hamming_distance <= 0:
            alt2 = self.generate_alternative()
            while alt1 == alt2:
                alt2 = self.generate_alternative()
        else:
            # Use Knuth's subset algorithm to compute
            alt2_lst = list(alt1.as_tuple())
            changes = random_k_subset(self.__features, hamming_distance)
            for idx in changes:
                nVal = random.randrange(self.__dom_size)
                while nVal == alt2_lst[idx]:
                    nVal = random.randrange(self.__dom_size)
                alt2_lst[idx] = nVal
                alt2 = Alternative(alt2_lst)
        return alt1, alt2

    def __len__(self) -> int:
        """
        Computes the total size of the domain.
        :return: The number of alternatives contained in the domain.
        """
        return self.size()
