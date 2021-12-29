from unittest import TestCase

from utils.primes import is_perfect_power, is_probably_prime, totient


class PrimesTest(TestCase):
    def test_totient_function(self):
        self.assertEqual(1, totient(1))
        self.assertEqual(6, totient(9))
        self.assertEqual(276, totient(277))

    def test_is_perfect_power(self):
        values = [(2, False), (4, True), (27, True), (28, False), (64, True)]

        for n, expected in values:
            self.assertEqual(
                expected,
                is_perfect_power(n),
            )

    def test_is_prime(self):
        values = [
            (0, False),
            (1, False),
            (2, True),
            (3, True),
            (4, False),
            (64, False),
            (7901, True),
            (7907, True),
            (7919, True),
            (8000, False),
            (27271, True),
            (1249591776595066706074168700537, True),
            (9007199254740991, False),
        ]

        for n, expected in values:
            self.assertEqual(
                expected,
                is_probably_prime(n),
                f"{n} expected to be {'prime' if expected else 'not prime'}",
            )
