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

    cipher_bytes = [ord(x) ^ ord(y) for x, y in zip(message, key)]
    return "".join([chr(b) for b in cipher_bytes])


def otp_decrypt(ciphertext: str, key: str) -> str:
    """
    Dectrypts the given message using the given key and the one-time pad scheme.
    A ValueError is raised if the length of the message and the key don't match.

    Each character is assumed to use 7 bits.
    """
    return otp_encrypt(ciphertext, key)
