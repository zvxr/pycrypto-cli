
import argparse
from crypto.classes.ciphers.aes import AESCipher
from crypto.classes.ciphers.xor import XORCipher
from crypto.classes.encoders.base import NullEncoder
from crypto.classes.encoders.binary import Base64Encoder, URLSafeBase64Encoder
from Crypto.Cipher import AES


CHAINING_MODES = {
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'CTR': AES.MODE_CTR,
    'ECB': AES.MODE_ECB,
    'OFB': AES.MODE_OFB,
    'OPENPGP': AES.MODE_OPENPGP
}
CHAINING_MODE_CHOICES = AES_MODES.keys()
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


def add_io_args(parser):
    """Add standard I/O arguments to ArgumentParser.
    Uses switches (d, v, x).
    """
    parser.add_argument(
        "--data",
        "-d",
        help="Raw (string) data to manipulate."
    )

    parser.add_argument(
        "--clipboard",
        "-v",
        action="store_true",
        help="Data is pulled/stored in clipboard."
    )

    parser.add_argument(
        "--clear-on-exit",
        "-x",
        action="store_true",
        help="When True will clear the screen when script completes."
    )


def add_cipher_args(parser):
    """Add cipher specific arguments to ArgumentParser.
    Adds positional argument 'cipher'.
    Uses optional switches (D, e, iv, k, m).
    """
    parser.add_argument(
        "cipher",
        "-c",
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
