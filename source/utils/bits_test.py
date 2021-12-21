from unittest import TestCase

from utils.bits import bits_as_str, bits_to_str, int_to_bits, str_to_bits, xor_bits


class BitsTest(TestCase):
    def test_int_to_bits(self):
        c_bits = int_to_bits(ord("C"), 7)
        self.assertEqual([1, 0, 0, 0, 0, 1, 1], c_bits)

    def test_int_to_bits_with_padding(self):
        c_bits = int_to_bits(ord("C"), 8)
        self.assertEqual([0, 1, 0, 0, 0, 0, 1, 1], c_bits)

    def test_display_bits(self):
        bits = [0, 1, 0, 0, 0, 0, 1, 1]
        self.assertEqual("01000011", bits_as_str(bits))

    def test_string_to_bits(self):
        string = "CS"
        self.assertEqual(
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1], str_to_bits(string)
        )

    def test_bits_to_string(self):
        bits = [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1]
        self.assertEqual("CS", bits_to_str(bits))

    def test_xor_bits(self):
        a = [1, 0, 1, 1, 0, 0, 1]
        b = [1, 0, 0, 1, 1, 1, 0]
        expected = [0, 0, 1, 0, 1, 1, 1]

        self.assertEqual(expected, xor_bits(a, b))
