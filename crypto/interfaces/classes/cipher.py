
from crypto.classes.ciphers.aes import AESCipher
from crypto.classes.ciphers.xor import XORCipher
from crypto.classes.encoders.base import NullEncoder
from crypto.classes.encoders.binary import Base64Encoder, URLSafeBase64Encoder
from Crypto.Cipher import AES
from crypto.interfaces.classes.base import DataInterface

CHAINING_MODES = {
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'CTR': AES.MODE_CTR,
    'ECB': AES.MODE_ECB,
    'OFB': AES.MODE_OFB
}
CHAINING_MODE_CHOICES = CHAINING_MODES.keys()
CHAINING_MODE_DEFAULT = "CFB"

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


class CipherInterface(DataInterface):
    def __init__(self, args):
        """args namespace should be derived from add_parser_args."""
        pass

    @staticmethod
    def add_parser_args(parser):
        """Add Cipher related arguments to ArgumentParser.
        Adds positional argument 'cipher'.
        Uses optional switches (D, e, iv, k, m).
        """
        parser.add_argument(
            "cipher",
            choices=CIPHER_CHOICES,
            default=CIPHER_DEFAULT,
            help="Cipher to apply. Choices:{}".format(CIPHER_CHOICES),
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
            help="Encoder/Decoder to apply to text when encrypting/decrypting. Choices:{}".format(
                ENCODER_CHOICES
            ),
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
            default=CHAINING_MODE_DEFAULT,
            help="Chaining mode to use. This applies only to AES cipher. Choices:{}".format(
                CHAINING_MODE_CHOICES
            ),
            type=str.upper
        )
