
import crypto.interfaces.commandline.base as base_cli
import time

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
        iv_gen=None,
        key=None,
        key_gen=None,
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
        self.decrypt = decrypt
        self.generated_key = False
        self.generated_iv = False

        if 'mode' in self.cipher.attributes and mode:
            self.cipher.set_mode(mode)

        if key:
            self.cipher.key = self.read_from_file(key)
        else:
            self.cipher.key = self.get_key(key_gen)

        if 'iv' in self.cipher.attributes:
            if iv:
                self.cipher.iv = self.read_from_file(iv)
            else:
                self.cipher.iv = self.get_iv(iv_gen)

        if encoder:
            self.cipher.set_encoding(ENCODERS[encoder])

    def execute(self):
        """Performs necessary encryption/decryption and associated writing operations."""
        epoch = "{}".format(int(time.time()))

        if self.generated_key:
            self.write_to_file("{}.key".format(epoch), self.cipher.key)
        if self.generated_iv:
            self.write_to_file("{}.iv".format(epoch), self.cipher.iv)

        if self.decrypt:
            print("DATA: {}".format(self.cipher.decrypt(self.data)))
        else:
            print("DATA: {}".format(self.cipher.encrypt(self.data)))

    def get_key(self, key_gen):
        """Calls and returns cipher's key generation method.
        If it doesn't exist, initiate a prompt.
        """
        if not self.decrypt and key_gen and hasattr(self.cipher, 'generate_key'):
            self.generated_key = True
            return self.cipher.generate_key()
        return self.get_from_prompt("Please enter a valid key: ")

    def get_iv(self, iv_gen):
        """Calls and returns cipher's IV generation method.
        It if doesn't exist, initiate a prompt.
        """
        if not self.decrypt and iv_gen and hasattr(self.cipher, 'generate_iv'):
            self.generated_iv = True
            return self.cipher.generate_iv()
        return self.get_from_prompt("Please enter a valid IV: ")


def execute(args):
    """Instantiates interface from argparse namespace and executes."""
    interface = CipherInterface(**vars(args))
    interface.execute()


def add_parser_args(parser):
    """Adds Cipher related arguments to ArgumentParser and sets execute method.
    Add positional argument 'cipher'.
    Uses optional switches (D, e, iv, IV, k, K, m).
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
        help="Path to initialization vector used to encrypt or decrypt. IV must adhere to constraints of cipher."
    )

    parser.add_argument(
        "--iv-gen",
        "-IV",
        action="store_true",
        default=False,
        help="Generate a random IV automatically."
    )

    parser.add_argument(
        "--key",
        "-k",
        help="Path to key used to encrypt or decrypt. Key size must adhere to constraints of cipher."
    )

    parser.add_argument(
        "--key-gen",
        "-K",
        action="store_true",
        default=False,
        help="Generate a random key automatically."
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=CHAINING_MODE_CHOICES,
        default=None,
        help="Chaining mode to use. This applies only to block ciphers.",
        type=str.upper
    )
