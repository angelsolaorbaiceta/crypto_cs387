import argparse
from hashlib import sha256

from block_cipher import CBCMode, ECMode

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
    parser.add_argument(
        "-m", "--mode", help="Mode of operation", choices=["ecb", "cbc"], default="ecb"
    )

    return parser


def get_cipher(mode_of_operation: str, key: bytes):
    if mode_of_operation == "ecb":
        return ECMode(key, BLOCK_SIZE_BYTES)

    elif mode_of_operation == "cbc":
        return CBCMode(key, BLOCK_SIZE_BYTES)

    else:
        raise ValueError(f"Unknown mode of operation: {mode_of_operation}")


if __name__ == "__main__":
    parser = init_arguments_parser()
    args = parser.parse_args()

    key = sha256(args.key.encode("utf-8")).digest()
    cipher = get_cipher(args.mode, key)

    if args.encrypt:
        print(f"Encrypting file with key: {key.hex()}")

        with open(args.in_file_path, "rb") as in_file:
            with open(f"{args.in_file_path}.enc", "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(cipher.encrypt_block(in_bytes))

    elif args.decrypt:
        with open(args.in_file_path, "rb") as in_file:
            with open(f"{args.in_file_path}.dec", "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(cipher.decrypt_block(in_bytes))

    else:
        parser.print_help()
        exit(1)
