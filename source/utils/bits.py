import operator
from functools import reduce
from typing import List

Bits = List[int]


def str_to_bits(string: str, length=7) -> Bits:
    """
    Returns the bits sequence representing the given string, using as many bits
    per character as the given length.
    """
    return reduce(operator.add, [int_to_bits(ord(char), length) for char in string])


def int_to_bits(n: int, length=7) -> Bits:
    """
    Creates the list of bits (a list of integers, either 0 or 1) for a given
    integer value using the provided length.

    If the bits can't fit into the provided length, it raises a ValueError.
    If the bits are less than the provided length, the list is padded using
    as many zeroes as required.
    """
    binary_str = format(n, "b")
    padding_len = length - len(binary_str)

    if padding_len < 0:
        raise ValueError(f"{binary_str} cannot fit in {length} bits")

    return [0] * padding_len + [int(n) for n in binary_str]


def bits_as_str(bits: Bits) -> str:
    """
    Produces the string representation of a given list of bits:
    bits_as_str([1, 0, 1]) => "101"
    """
    return "".join(map(str, bits))
