from unittest import TestCase

from utils.primes import totient


class PrimesTest(TestCase):
    def test_totient_function(self):
        self.assertEqual(1, totient(1))
        self.assertEqual(6, totient(9))
        self.assertEqual(276, totient(277))
