
import argparse

from crypto.interfaces.classes.base import DataInterface
from crypto.interfaces.classes.cipher import CipherInterface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        conflict_handler="resolve",
        prog="pycrypto-cli"
    )
    mode_parser = parser.add_subparsers(
        help="Pycrypto module to use."
    )

    data_parser = argparse.ArgumentParser(add_help=False)
    DataInterface.add_parser_args(data_parser)

    cipher_parser = mode_parser.add_parser(
        "cipher",
        parents=[data_parser],
        help="Use cipher module."
    )
    CipherInterface.add_parser_args(cipher_parser)

    hash_parser = mode_parser.add_parser(
        "hash",
        parents=[data_parser],
        help="Use hash module."
    )

    # Debugging for now.
    args = parser.parse_args()
    import pdb; pdb.set_trace()
    print args
