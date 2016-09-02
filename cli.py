
import argparse
import crypto.interfaces.commandline.argparser as cli_parsers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    mode_parser = parser.add_subparsers(help="Pycrypto module to use.")

    data_parser = argparse.ArgumentParser(add_help=False)
    cli_parsers.add_data_parser_args(data_parser)

    cipher_parser = mode_parser.add_parser("cipher", parents=[data_parser], help="Use cipher module.")
    cli_parsers.add_cipher_parser_args(cipher_parser)

    hash_parser = mode_parser.add_parser("hash", parents=[data_parser], help="Use hash module.")

    # Debugging for now.
    args = parser.parse_args()
    print args
