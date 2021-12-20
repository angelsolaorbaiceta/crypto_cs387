from utils.bits import str_to_bits, bits_to_str


def otp_encrypt(message: str, key: str) -> str:
    """
    Encrypts the given message using the given key and the one-time pad scheme.
    A ValueError is raised if the length of the message and the key don't match.

    Each character is assumed to use 7 bits.
    """
    if len(message) != len(key):
        raise ValueError(
            f"The lengths of the message ({len(message)}) and the key ({len(key)} don't match)"
        )

    msg_bits = str_to_bits(message)
    key_bits = str_to_bits(key)
    cipher_bits = [x ^ y for x, y in zip(msg_bits, key_bits)]

    return bits_to_str(cipher_bits)


def otp_decrypt(ciphertext: str, key: str) -> str:
    """
    Dectrypts the given message using the given key and the one-time pad scheme.
    A ValueError is raised if the length of the message and the key don't match.

    Each character is assumed to use 7 bits.
    """
    return otp_encrypt(ciphertext, key)
