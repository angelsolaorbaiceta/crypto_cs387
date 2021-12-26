import argparse
from hashlib import sha256

# Blocks of 32 bytes = 256 bits.
BLOCK_SIZE_BYTES = 32


def init_arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] < <file>",
        description="Encrypts or decrypts the file passed as standard input.",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"{parser.prog} v1.0.0"
    )
    enc_dec = parser.add_mutually_exclusive_group(required=True)
    enc_dec.add_argument(
        "-e",
        "--encrypt",
        help="Encrypt a file",
        dest="encrypt",
        action="store_true",
        default=False,
    )
    enc_dec.add_argument(
        "-d",
        "--decrypt",
        help="Decrypt a file",
        dest="decrypt",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f", "--file", help="Path to file", dest="in_file_path", required=True
    )
    parser.add_argument(
        "-k",
        "--key",
        help="Key for the encryption/decryption",
        dest="key",
        required=True,
    )

    return parser


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    if len(plaintext) > len(key):
        raise ValueError("plaintext block larger than key")

    return bytes([p ^ k for p, k in zip(plaintext, key)])


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return encrypt(ciphertext, key)


if __name__ == "__main__":
    parser = init_arguments_parser()
    args = parser.parse_args()

    key = sha256(args.key.encode("utf-8")).digest()

    if args.encrypt:
        with open(args.in_file_path, "rb") as in_file:
            with open(f"{args.in_file_path}.enc", "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(encrypt(in_bytes, key))

    elif args.decrypt:
        with open(args.in_file_path, "rb") as in_file:
            with open(f"{args.in_file_path}.dec", "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(decrypt(in_bytes, key))

    else:
        parser.print_help()
        exit(1)
