"""Counting theory functions used by the analyzer."""

from math import factorial
from itertools import product


def rule_of_product(sigma, n):
    """Number of strings of length n from an alphabet of size sigma."""
    return sigma ** n


def permutations(m, n):
    """P(m,n) = m! / (m-n)!; returns 0 when n > m."""
    if n < 0 or m < 0 or n > m:
        return 0
    return factorial(m) // factorial(m - n)


def combinations(m, n):
    """C(m,n) = m! / (n! * (m-n)!); returns 0 for invalid inputs."""
    if n < 0 or m < 0 or n > m:
        return 0
    return factorial(m) // (factorial(n) * factorial(m - n))


def inclusion_exclusion_count(n, class_sizes):
    """Count length-n strings containing at least one character of every class."""
    if n < 0 or any(size < 0 for size in class_sizes):
        return 0

    class_count = len(class_sizes)
    total_sigma = sum(class_sizes)
    total = 0

    for mask in range(1 << class_count):
        removed = 0
        selected_classes = 0

        for index in range(class_count):
            if mask & (1 << index):
                removed += class_sizes[index]
                selected_classes += 1

        remaining = total_sigma - removed
        term = remaining ** n

        if selected_classes % 2 == 0:
            total += term
        else:
            total -= term

    return total


def brute_force_check():
    """Check the rule of product using a small alphabet {a, b} and n=3."""
    alphabet = ["a", "b"]
    n = 3
    brute_force_total = len(list(product(alphabet, repeat=n)))
    formula_total = rule_of_product(len(alphabet), n)
    return brute_force_total, formula_total, brute_force_total == formula_total
