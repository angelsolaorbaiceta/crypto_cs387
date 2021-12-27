from unittest import TestCase

from symmetric.block_cipher import CTRMode

BLOCK_SIZE_BYTES = 2

# key = 'ab'
KEY = bytes([0x61, 0x62])

# nonce = 'cd'
NONCE = bytes([0x63, 0x64])

# plaintext = 'Lore' (len = 4, 2 blocks)
PLAINTEXT = bytes([0x4C, 0x6F, 0x72, 0x65])


class TestCounterMode(TestCase):
    ciphertext = bytes([0x4E, 0xC, 0x70, 0x5])

    def setUp(self):
        self.cipher_executor = CTRMode(
            key=KEY, nonce=NONCE, block_size_bytes=BLOCK_SIZE_BYTES
        )

    def test_encrypt(self):
        cipher_0 = self.cipher_executor.encrypt_block(PLAINTEXT[0:2])
        self.assertEqual(self.ciphertext[0:2], cipher_0)

        cipher_1 = self.cipher_executor.encrypt_block(PLAINTEXT[2:4])
        self.assertEqual(self.ciphertext[2:4], cipher_1)

    def test_decrypt(self):
        plain_0 = self.cipher_executor.decrypt_block(self.ciphertext[0:2])
        self.assertEqual(PLAINTEXT[0:2], plain_0)

        plain_1 = self.cipher_executor.decrypt_block(self.ciphertext[2:4])
        self.assertEqual(PLAINTEXT[2:4], plain_1)
