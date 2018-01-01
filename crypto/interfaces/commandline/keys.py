
import crypto.interfaces.commandline.base as base_cli
import time

import crypto.classes.keys.rsa as rsa


KEY_CHOICES = ("RSA",)
KEY_DEFAULT = "RSA"
KEYS = {
    'RSA': rsa
}


class KeysInterface(base_cli.Interface):
    """Class for commandline interface that deals with generating keys,
    specifically.
    """
    def __init__(
        self,
        algorithm,
        data_output_path=None,
        key_format=None,
        *args,
        **kwargs
    ):
        super(KeysInterface, self).__init__()

        self.algorithm = algorithm
        self.key_format = key_format
        self.set_data_output(data_output_path)

    def execute(self):
        """Performs necessary encryption/decryption and associated writing
        operations.
        """
        pass

    def set_data_output(self, data_output_path):
        """Stores the method to be called for generating store_data. Writing to
        file `data_output_path` takes highest priority. Lowest priority is to
        print to screen.
        """
        if data_output_path:
            self.store_data = lambda data: self.write_to_file(
                data_output_path,
                data
            )
            return

        self.store_data = lambda data: print("DATA: {}".format(data))


def execute(args):
    """Instantiates interface from argparse namespace and executes."""
    interface = KeysInterface(**vars(args))
    interface.execute()


def add_parser_args(parser):
    """Adds Cipher related arguments to ArgumentParser and sets execute method.
    Add positional argument 'algorithm'.
    Uses optional switches (f, o).
    """
    parser.set_defaults(execute=execute)

    parser.add_argument(
        "algorithm",
        choices=KEY_CHOICES,
        default=KEY_DEFAULT,
        help="Key algorithm to apply.",
        type=str.upper
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=KEY_FORMATS,
        dest="key_format",
        help="The format of the key.",
    )

    parser.add_argument(
        "--output",
        "-o",
        dest="data_output_path",
        help="Path to file to write data out to."
    )
