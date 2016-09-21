
import crypto.interfaces.commandline.base as base_cli

from crypto.classes.ciphers.aes import AESCipher
from crypto.classes.ciphers.xor import XORCipher
from crypto.classes.encoders.base import NullEncoder
from crypto.classes.encoders.binary import Base64Encoder, URLSafeBase64Encoder
from Crypto.Cipher import AES


CHAINING_MODE_CHOICES = set(AESCipher.supported_modes.keys())

CIPHERS = {
    'AES': AESCipher,
    'XOR': XORCipher
}
CIPHER_CHOICES = CIPHERS.keys()
CIPHER_DEFAULT = "XOR"

ENCODERS = {
    'BASE64': Base64Encoder,
    'NULL': NullEncoder,
    'URLSAFEBASE64': URLSafeBase64Encoder,
}
ENCODER_CHOICES = ENCODERS.keys()
ENCODER_DEFAULT = "BASE64"


class CipherInterface(base_cli.DataInterface):
    def __init__(
        self,
        cipher,
        clear_on_exit=None,
        clipboard_input=None,
        clipboard_output=None,
        data=None,
        decrypt=None,
        encoder=None,
        iv=None,
        key=None,
        mode=None,
        *args,
        **kwargs
    ):
        """Sets up the cipher itself when initializing."""
        super(CipherInterface, self).__init__(
            clear_on_exit,
            clipboard_input,
            clipboard_output,
            data
        )
        self.cipher = CIPHERS[cipher]()
        self.cipher.data = self.get_data()
        self.cipher.key = self.get_key() if not key else key
        self.decrypt = decrypt

        if 'iv' in self.cipher.attributes:
            self.cipher.iv = self.get_iv() if not iv else iv

        if 'mode' in self.cipher.attributes and mode:
            self.cipher.set_mode(mode)

        if encoder:
            self.cipher.set_encoding(ENCODERS[encoder])

    def execute(self):
        print("KEY:  {}".format(repr(self.cipher.key)))
        if hasattr(self.cipher, 'iv'):
            print("IV:   {}".format(repr(self.cipher.iv)))
        if self.decrypt:
            print("DATA: {}".format(repr(self.cipher.decrypt(self.data))))
        else:
            print("DATA: {}".format(repr(self.cipher.encrypt(self.data))))

    def get_key(self):
        """If cipher can generate keys, prompts user if they want key auto-generated.
        Otherwise initiates a prompt (value from user input).
        """
        if hasattr(self.cipher, 'generate_key') and self.get_bool_from_prompt("Auto-generate key?"):
            return self.cipher.generate_key()
        return self.get_from_prompt("Please enter a valid key: ")

    def get_iv(self):
        """If cipher can generate IVs, prompts user if they want IV auto-generated.
        Otherwise initiates a prompt (value from user input).
        """
        if hasattr(self.cipher, 'generate_iv') and self.get_bool_from_prompt("Auto-generate IV?"):
            return self.cipher.generate_iv()
        return self.get_from_prompt("Please enter a valid IV: ")


def execute(args):
    """Instantiates interface from argparse namespace and executes."""
    interface = CipherInterface(**vars(args))
    interface.execute()


def add_parser_args(parser):
    """Adds Cipher related arguments to ArgumentParser and sets execute method.
    Add positional argument 'cipher'.
    Uses optional switches (D, e, iv, k, m).
    """
    parser.set_defaults(execute=execute)

    parser.add_argument(
        "cipher",
        choices=CIPHER_CHOICES,
        default=CIPHER_DEFAULT,
        help="Cipher algorithm to apply.",
        type=str.upper
    )

    parser.add_argument(
        "--decrypt",
        "-D",
        action="store_true",
        default=False,
        help="When True will decrypt data. When False will encrypt data."
    )

    parser.add_argument(
        "--encoder",
        "-e",
        choices=ENCODER_CHOICES,
        default=ENCODER_DEFAULT,
        help="Encoder/Decoder to apply to text when encrypting/decrypting.",
        type=str.upper
    )

    parser.add_argument(
        "--iv",
        "-iv",
        help="Initialization vector "
    )

    parser.add_argument(
        "--key",
        "-k",
        help="Key used to encrypt or decrypt. Key size must adhere to constraints of cipher."
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=CHAINING_MODE_CHOICES,
        default=None,
        help="Chaining mode to use. This applies only to block ciphers.",
        type=str.upper
    )
