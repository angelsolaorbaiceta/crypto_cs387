# 256 bits
BLOCK_SIZE_BYTES = 32


def _xor_bytes(plaintext: bytes, key: bytes) -> bytes:
    return bytes([p ^ k for p, k in zip(plaintext, key)])


class ECMode:
    """
    Electronic Codebook mode of operation implementation of a block cipher.
    """

    def __init__(self, key: bytes, block_size_bytes=BLOCK_SIZE_BYTES):
        if len(key) != block_size_bytes:
            raise ValueError("Block and key sizes should be equal")

        self.__block_size_bytes = block_size_bytes
        self.__key = key

    def encrypt_block(self, block: bytes) -> bytes:
        return _xor_bytes(block, self.__key)

    def decrypt_block(self, block: bytes) -> bytes:
        return _xor_bytes(block, self.__key)


class CBCMode:
    """
    Cipher Block Chaining mode of operation implementation of a block cipher.
    """

    def __init__(self, key: bytes, block_size_bytes=BLOCK_SIZE_BYTES):
        if len(key) != block_size_bytes:
            raise ValueError("Block and key sizes should be equal")

        self.__block_size_bytes = block_size_bytes
        self.__key = key

    def encrypt_block(self, block: bytes) -> bytes:
        return block

    def decrypt_block(self, block: bytes) -> bytes:
        return block
