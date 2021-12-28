from math import gcd


def totient(n: int) -> int:
    """
    The totient function returns the number of positive integers smaller than n
    that are relatively prime to n.

    Two positive integers are said to be "relatively prime" if their greatest
    common divisor is 1.

    See: https://en.wikipedia.org/wiki/Euler%27s_totient_function.
    """
    # TODO: if n is prime, then totient(n) = n-1
    count = 0

    for i in range(1, n + 1):
        if are_rel_prime(i, n):
            count += 1

    return count


def are_rel_prime(a: int, b: int) -> bool:
    """
    Checks whether two integers are relatively prime, that is, if their greates
    common divisor is 1.
    """
    return gcd(a, b) == 1
