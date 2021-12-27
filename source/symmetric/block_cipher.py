# 256 bits
BLOCK_SIZE_BYTES = 32


def _xor_bytes(seq_a: bytes, seq_b: bytes) -> bytes:
    return bytes([a ^ b for a, b in zip(seq_a, seq_b)])


class ECMode:
    """
    Electronic Codebook mode of operation implementation of a block cipher.

    Both the encryption and decryption methods expect the blocks in order:
    b0, b1, b2, ...
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

    def __repr__(self) -> str:
        return f"ECB mode, block size = {self.__block_size_bytes} bytes, key = {self.__key.hex()}"


class CBCMode:
    """
    Cipher Block Chaining mode of operation implementation of a block cipher.

    TODO: missing IV (initialization vector) to encrypt the first block.

    The encryption method expects the plaintext blocks in order:
    m0, m1, m2, ...

    and the ciphertext blocks also in order:
    c0, c1, c2, ...
    """

    def __init__(self, key: bytes, block_size_bytes=BLOCK_SIZE_BYTES):
        if len(key) != block_size_bytes:
            raise ValueError("Block and key sizes should be equal")

        self.__block_size_bytes = block_size_bytes
        self.__key = key
        self.__last_block = None

    def encrypt_block(self, block: bytes) -> bytes:
        if self.__last_block is None:
            self.__last_block = _xor_bytes(block, self.__key)
        else:
            m_xor_c = _xor_bytes(block, self.__last_block)
            self.__last_block = _xor_bytes(m_xor_c, self.__key)

        return self.__last_block

    def decrypt_block(self, block: bytes) -> bytes:
        plaintext = (
            _xor_bytes(block, self.__key)
            if self.__last_block is None
            else _xor_bytes(_xor_bytes(block, self.__key), self.__last_block)
        )
        self.__last_block = block

        return plaintext

    def __repr__(self) -> str:
        return f"CBC mode, block size = {self.__block_size_bytes} bytes, key = {self.__key.hex()}"
