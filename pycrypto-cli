#!/usr/bin/env python2.7

import argparse
import crypto.interfaces.commandline.base as base_cli
import crypto.interfaces.commandline.cipher as cipher_cli


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        conflict_handler="resolve",
        prog="pycrypto-cli"
    )
    mode_parser = parser.add_subparsers(
        help="Pycrypto module to use."
    )

    data_parser = argparse.ArgumentParser(add_help=False)
    base_cli.add_parser_args(data_parser)

    cipher_parser = mode_parser.add_parser(
        "cipher",
        parents=[data_parser],
        help="Use cipher module."
    )
    cipher_cli.add_parser_args(cipher_parser)

    hash_parser = mode_parser.add_parser(
        "hash",
        parents=[data_parser],
        help="Use hash module."
    )

    # Debugging for now.
    args = parser.parse_args()
    args.execute(args)
