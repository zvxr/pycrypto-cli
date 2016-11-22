
import crypto.interfaces.commandline.base as base_cli
import time

from crypto.classes.ciphers.aes import AESCipher
from crypto.classes.ciphers.blowfish import BlowfishCipher
from crypto.classes.ciphers.xor import XORCipher
from crypto.classes.encoders.base import NullEncoder
from crypto.classes.encoders.binary import Base64Encoder, URLSafeBase64Encoder


CHAINING_MODE_CHOICES = set(
    AESCipher.supported_modes.keys() + BlowfishCipher.supported_modes.keys()
)

CIPHERS = {
    'AES': AESCipher,
    'BLOWFISH': BlowfishCipher,
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
        clipboard_input=None,
        clipboard_output=None,
        data_input_path=None,
        data_output_path=None,
        decrypt=None,
        encoder=None,
        iv_gen=None,
        iv_path=None,
        key_gen=None,
        key_path=None,
        mode=None,
        *args,
        **kwargs
    ):
        """Sets up the cipher itself when initializing."""
        super(CipherInterface, self).__init__(
            clipboard_input,
            clipboard_output,
            data_input_path,
            data_output_path
        )
        self.cipher = CIPHERS[cipher]()
        self.cipher.data = self.data
        self.decrypt = decrypt
        self.generated_key = False
        self.generated_iv = False

        self.set_mode(mode)
        self.set_key(key_gen, key_path)
        self.set_iv(iv_gen, iv_path)
        self.set_encoder(encoder)

    def execute(self):
        """Performs necessary encryption/decryption and associated writing operations."""
        epoch = "{}".format(int(time.time()))

        if self.generated_key:
            self.write_to_file("{}.key".format(epoch), self.cipher.key)
        if self.generated_iv:
            self.write_to_file("{}.iv".format(epoch), self.cipher.iv)

        if self.decrypt:
            self.store_data(self.cipher.decrypt(self.data))
        else:
            self.store_data(self.cipher.encrypt(self.data))

    def set_encoder(self, encoder):
        """Set the cipher's encoder."""
        if encoder:
            self.cipher.set_encoding(ENCODERS[encoder])

    def set_key(self, key_gen, key_path):
        """Determine and set cipher's key. Reading file `key_path` takes highest
        priority. When `key_gen` is True, will generate a key instead. Lowest
        priority is to fetch the key from a commandline prompt.
        """
        if key_path:
            self.cipher.key = self.read_from_file(key_path)
            return

        if not self.decrypt and key_gen and hasattr(self.cipher, 'generate_key'):
            self.generated_key = True
            self.cipher.key = self.cipher.generate_key()
            return

        self.cipher.key = self.get_from_prompt("Please enter a valid key: ")

    def set_iv(self, iv_gen, iv_path):
        """Determine and set cipher's IV if appropriate. Reading file `iv_path`
        takes highest priority. When `iv_gen` is True, will generate an IV instead.
        Lowest priority is to fetch the IV from a commandline prompt.
        """
        if 'iv' not in self.cipher.attributes:
            return

        if iv_path:
            self.cipher.iv = self.read_from_file(iv_path)
            return

        if not self.decrypt and iv_gen and hasattr(self.cipher, 'generate_iv'):
            self.generated_iv = True
            self.cipher.iv = self.cipher.generate_iv()
            return

        self.cipher.iv = self.get_from_prompt("Please enter a valid IV: ")

    def set_mode(self, mode):
        """Set the cipher's mode if appropriate."""
        if 'mode' in self.cipher.attributes and mode:
            self.cipher.set_mode(mode)


def execute(args):
    """Instantiates interface from argparse namespace and executes."""
    interface = CipherInterface(**vars(args))
    interface.execute()


def add_parser_args(parser):
    """Adds Cipher related arguments to ArgumentParser and sets execute method.
    Add positional argument 'cipher'.
    Uses optional switches (d, e, iv, IV, k, K, m).
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
        "-d",
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
        dest="iv_path",
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
        dest="key_path",
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
