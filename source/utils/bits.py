from itertools import zip_longest
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
    Produces the string representation of the numbers in a given list of bits:
    bits_as_str([1, 0, 1]) => "101"
    """
    return "".join(map(str, bits))


def bits_to_char(bits: Bits) -> str:
    """
    Returns the char whose ASCII code is the given value given as a sequence of bits.
    """
    return chr(int(bits_as_str(bits), 2))


def bits_to_str(bits: Bits, char_length=7) -> str:
    """
    Produces the string of the given bit sequence, assuming a given length used to
    encode each character.

    Raises a ValueError if the number of bits isn't a multiple of the length.
    """
    if len(bits) % char_length != 0:
        raise ValueError(
            f"Expected the bits length ({len(bits)}) to be a multiple of {char_length}"
        )

    return "".join([bits_to_char(bits) for bits in __grouper(bits, char_length)])


def xor_bits(a: Bits, b: Bits) -> Bits:
    """
    Applies a bitwise XOR, creating a new sequence of bits from the two input sequences.
    Raises a ValueError if the two sequences don't match in size.
    """
    if len(a) != len(b):
        raise ValueError(
            f"Expected bit sequences to have the same length: {len(a)} != {len(b)}"
        )

    return [x ^ y for x, y in zip(a, b)]


def __grouper(iterable, n: int, fillvalue=None):
    """
    Collect data into non-overlapping fixed-length chunks or blocks
    Recipe from https://docs.python.org/3/library/itertools.html.

    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
