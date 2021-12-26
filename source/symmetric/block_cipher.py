import sys

# 256 bits
BLOCK_SIZE_BYTES = 32


def encrypt(bytes, fn):
    st = sys.stdin.buffer.read(BLOCK_SIZE_BYTES)
