from math import floor, gcd, log2
from random import randint

from utils.numbers import is_even


def totient(n: int) -> int:
    """
    The totient function returns the number of positive integers smaller than n
    that are relatively prime to n.

    Two positive integers are said to be "relatively prime" if their greatest
    common divisor is 1.

    When a number n is prime, its totient is n - 1.

    Whena a number n is the product of two prime numbers p and q, its totien
    function is the product of the two factor's totients: totient(p) * totient(q).

    See: https://en.wikipedia.org/wiki/Euler%27s_totient_function.
    """
    if is_probably_prime(n):
        return n - 1

    count = 0
    for i in range(1, n + 1):
        if are_coprime(i, n):
            count += 1

    return count


def are_coprime(a: int, b: int) -> bool:
    """
    Checks whether two integers are relatively prime or coprime, that is, if
    their greatest common divisor is 1.
    """
    return gcd(a, b) == 1


def is_probably_prime(n: int, rounds: int = 10) -> bool:
    """
    Checks whether a positive integer is probably prime using the Miller-Rabin
    primality test. The more rounds are given for testing the number's
    primality, the higher the confidence of it being prime.

    See: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    if n < 0:
        raise ValueError(
            f"Can't check whether {n} is prime: expected a positive integer."
        )

    if n == 0 or n == 1:
        return False

    if n == 2 or n == 3:
        return True

    if is_even(n):
        return False

    n_minus_one = n - 1
    factors = _rabin_miller_factorization(n_minus_one)
    r = factors.count(2)
    d = factors[-1]

    def loop(x: int):
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n_minus_one:
                return True

        return False

    for _ in range(rounds):
        base = randint(2, n - 2)
        x = pow(base, d, n)

        if x == 1 or x == n_minus_one:
            continue

        if loop(x):
            continue

        return False

    return True


def _rabin_miller_factorization(n: int):
    """
    Returns the factorization of a number to be used in the Rabin-Miller primality
    test.

    >>> _rabin_miller_factorization(220)
    >>> [2, 2, 55]
    """
    factors = []

    while is_even(n):
        factors.append(2)
        n //= 2

    return factors + [n]


def is_perfect_power(n: int) -> bool:
    """
    Checks a given integer n can be expressed as the power of two numbers a**b
    where both a and b are integer numbers greater than 1.
    """
    if n < 4:
        return False

    for b in range(2, floor(log2(n)) + 1):
        a = n ** (1 / b)
        if a.is_integer():
            return True

    return False
