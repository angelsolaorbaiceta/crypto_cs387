import argparse
from hashlib import sha256

from block_cipher import CBCMode, ECMode, CTRMode

# Blocks of 32 bytes = 256 bits.
BLOCK_SIZE_BYTES = 32


def init_arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS] -f <file> -k <key>",
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
        "-n",
        "--nonce",
        help="Nonce used in the CTR mode of operation",
        dest="nonce",
        required=False,
    )
    parser.add_argument(
        "-iv",
        "--iv",
        help="Initialization vector used in the CBC mode of operation",
        dest="iv",
        required=False,
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode of operation",
        choices=["ecb", "cbc", "ctr"],
        default="ecb",
    )

    return parser


def get_cipher(mode_of_operation: str, key: bytes, nonce: bytes, iv: bytes):
    if mode_of_operation == "ecb":
        return ECMode(key, BLOCK_SIZE_BYTES)

    elif mode_of_operation == "cbc":
        return CBCMode(key, iv, BLOCK_SIZE_BYTES)

    elif mode_of_operation == "ctr":
        return CTRMode(key, nonce, BLOCK_SIZE_BYTES)

    else:
        raise ValueError(f"Unknown mode of operation: {mode_of_operation}")


if __name__ == "__main__":
    parser = init_arguments_parser()
    args = parser.parse_args()

    key = sha256(args.key.encode("utf-8")).digest()
    nonce = sha256(args.nonce.encode("utf-8")).digest() if args.nonce else None
    iv = sha256(args.iv.encode("utf-8")).digest() if args.iv else None
    cipher = get_cipher(args.mode, key, nonce, iv)

    if args.encrypt:
        print(f"Encrypting file: {cipher}")
        out_file_path = f"{args.in_file_path}.enc"

        with open(args.in_file_path, "rb") as in_file:
            with open(out_file_path, "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(cipher.encrypt_block(in_bytes))

        print(f"Encryption done: {out_file_path}")

    elif args.decrypt:
        print(f"Decrypting file: {cipher}")
        out_file_path = f"{args.in_file_path}.dec"

        with open(args.in_file_path, "rb") as in_file:
            with open(out_file_path, "wb") as file:
                while in_bytes := in_file.read(BLOCK_SIZE_BYTES):
                    file.write(cipher.decrypt_block(in_bytes))

        print(f"Decryption done: {out_file_path}")

    else:
        parser.print_help()
        exit(1)
