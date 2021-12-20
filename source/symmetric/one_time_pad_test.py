from unittest import TestCase
from symmetric.one_time_pad import otp_decrypt, otp_encrypt


class OneTimePadTest(TestCase):
    message = "CS"
    key = "np"
    ciphertext = "-#"

    def test_encrypt(self):
        self.assertEqual(self.ciphertext, otp_encrypt(self.message, self.key))

    def test_decrypt(self):
        self.assertEqual(self.message, otp_decrypt(self.ciphertext, self.key))
