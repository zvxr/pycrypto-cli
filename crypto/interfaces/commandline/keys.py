
import crypto.interfaces.commandline.base as base_cli
import time

import crypto.classes.keys.rsa as rsa


KEY_CHOICES = ("RSA",)
KEY_DEFAULT = "RSA"


class KeysInterface(base_cli.Interface):
    def __init__(
        self,
        keys_algorithm,
        clipboard=None,
        data_input_path=None,
        data_output_path=None,
        *args,
        **kwargs
    ):
        """Sets up the key algorithm itself when initializing."""
        self.keys_algorithm = 

    def execute(self):
        """Performs necessary encryption/decryption and associated writing operations."""
        pass


def execute(args):
    """Instantiates interface from argparse namespace and executes."""
    interface = KeysInterface(**vars(args))
    interface.execute()


def add_parser_args(parser):
    """Adds Cipher related arguments to ArgumentParser and sets execute method.
    Add positional argument 'cipher'.
    Uses optional switches ().
    """
    parser.set_defaults(execute=execute)

    parser.add_argument(
        "keys_algorithm",
        choices=KEY_CHOICES,
        default=KEY_DEFAULT,
        help="Key algorithm to apply.",
        type=str.upper
    )
