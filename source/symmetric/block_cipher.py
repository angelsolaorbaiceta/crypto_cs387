# 256 bits
BLOCK_SIZE_BYTES = 32


def _xor_bytes(seq_a: bytes, seq_b: bytes) -> bytes:
    return bytes([a ^ b for a, b in zip(seq_a, seq_b)])


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

    def __repr__(self) -> str:
        return (
            f"ECB mode"
            + f"\n  block size = {self.__block_size_bytes} bytes"
            + f"\n  key = {self.__key.hex()}"
        )


class CBCMode:
    """
    Cipher Block Chaining mode of operation implementation of a block cipher.

    TODO: missing IV (initialization vector) to encrypt the first block.
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
        return (
            f"CBC mode"
            + f"\n  block size = {self.__block_size_bytes} bytes"
            + f"\n  key = {self.__key.hex()}"
        )


class CTRMode:
    """
    Counter mode of operation implementation of a block cipher.
    """

    @property
    def __nonced_counter(self):
        """
        Result of appending the first bytes of the nonce with the counter value.

        If the nonce is None, it simply uses the entire block size to encode the
        counter value.
        """
        if self.__nonce is None:
            return self.__counter.to_bytes(self.__block_size_bytes, "big")
        else:
            return self.__nonce[: self.__half_block_size] + self.__counter.to_bytes(
                self.__half_block_size, "big"
            )

    def __init__(
        self, key: bytes, nonce: bytes = None, block_size_bytes=BLOCK_SIZE_BYTES
    ):
        if len(key) != block_size_bytes:
            raise ValueError("Block and key sizes should be equal")

        if nonce and len(nonce) < block_size_bytes:
            raise ValueError("Nonce and block sizes should be equal")

        self.__block_size_bytes = block_size_bytes
        self.__half_block_size = block_size_bytes // 2
        self.__key = key
        self.__nonce = nonce
        self.__counter = 0

    def encrypt_block(self, block: bytes) -> bytes:
        self.__counter += 1
        return _xor_bytes(_xor_bytes(self.__nonced_counter, self.__key), block)

    def decrypt_block(self, block: bytes) -> bytes:
        self.__counter += 1
        return _xor_bytes(block, _xor_bytes(self.__nonced_counter, self.__key))

    def __repr__(self) -> str:
        return (
            f"CTR mode"
            + f"\n  block size = {self.__block_size_bytes} bytes"
            + f"\n  key = {self.__key.hex()}"
            + f"\n  nonce = {self.__nonce.hex() if self.__nonce else 'None'}"
        )
