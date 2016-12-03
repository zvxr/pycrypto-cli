
from collections import namedtuple
from crypto.classes.encoders.base import Encoder
from Crypto import Random
from Crypto.Cipher import blockalgo
from Crypto.Util import Counter


BlockCipherMode = namedtuple('BlockCipherMode', ('mode_id', 'requires_iv', 'uses_counter'))


class CryptoCipher(object):
    """Base Class for Ciphers."""
    attributes = ('key',)

    def __init__(self, key=None):
        self._key = key
        self._encoder = None
        self._decoder = None

    def __repr__(self):
        return "{} key {} set.".format(
            self.__class__,
            "is" if self._key is not None else "is not"
        )

    @property
    def key(self):
        if self._key is not None:
            return self._key
        raise AttributeError("Key is not set.")

    @key.setter
    def key(self, value):
        self._key = value

    def _encode(self, text, *args, **kwargs):
        """Apply encode method to text and return"""
        if hasattr(self._encoder, "__call__"):
            return self._encoder(text, *args, **kwargs)
        else:
            return text

    def _decode(self, text, *args, **kwargs):
        """Apply decode method to text and return."""
        if hasattr(self._decoder, "__call__"):
            return self._decoder(text, *args, **kwargs)
        else:
            return text

    def encrypt(self, plaintext):
        raise NotImplementedError("Method not defined.")

    def decrypt(self, ciphertext):
        raise NotImplementedError("Method not defined.")

    def set_encoding(self, encoder):
        """Set encoder and decoder methods to be applied to text when encrypting
        and decrypting.
        """
        if not isinstance(encoder, Encoder):
            raise TypeError("Encoder")
        self._encoder = encoder.encode
        self._decoder = encoder.decode


class BlockCipher(CryptoCipher):
    """Base Class for Block Ciphers."""
    attributes = ('key', 'iv', 'mode')
    block_size = 0
    cipher_function = None
    default_mode = 'ECB'
    supported_modes = {
        'CBC': BlockCipherMode(blockalgo.MODE_CBC, True, False),
        'CFB': BlockCipherMode(blockalgo.MODE_CFB, True, False),
        'CTR': BlockCipherMode(blockalgo.MODE_CTR, False, True),
        'ECB': BlockCipherMode(blockalgo.MODE_ECB, False, False),
        'OFB': BlockCipherMode(blockalgo.MODE_OFB, True, False)
    }

    def __init__(self, key=None, iv=None, initial_value=1):
        super(BlockCipher, self).__init__(key)
        self._mode = self.supported_modes[self.default_mode]
        self._iv = iv
        self.initial_value = initial_value

    def __repr__(self):
        return "{} key {} set, IV {} set.".format(
            self.__class__,
            "is" if self._key is not None else "is not",
            "is" if self._iv is not None else "is not"
        )

    @property
    def iv(self):
        if not self.mode.requires_iv:
            return

        if self._iv is not None:
            return self._iv

        raise AttributeError("IV is not set.")

    @iv.setter
    def iv(self, value):
        if not self.mode.requires_iv:
            return

        if value is not None and len(value) != self.block_size:
            raise AttributeError(
                "iv must be {} bytes long.".format(self.block_size)
            )
        self._iv = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        """Set chaining mode by mapping mode (string) to object's supported modes."""
        if value not in self.supported_modes:
            raise AttributeError("Chaining mode not supported.")
        self._mode = self.supported_modes[value]

    def _get_cipher(self):
        """Return a stateful cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self.mode.uses_counter:
            return self.cipher.new(self.key, self.mode.mode_id, counter=self._get_counter())
        elif self.mode.requires_iv:
            return self.cipher.new(self.key, self.mode.mode_id, self.iv)
        else:
            return self.cipher.new(self.key, self.mode.mode_id)

    def _get_counter(self):
        """Returns a stateful Counter instance. Uses Pycrypto's incrementing function,
        where each counter block size is equal to the forward cipher's block size (in bytes).
        No prefix or suffix is applied; wrap arounds are disallowed to ensure uniqueness.
        """
        return Counter.new(
            self.cipher.block_size * 8,
            initial_value=self.initial_value,
            allow_wraparound=False
        )

    def _get_pad_char(self, ignore=None):
        """Return a random character to pad text that does not match ignore."""
        random_device = Random.new()
        while True:
            char = random_device.read(1)
            if char != ignore:
                return char

    def decrypt(self, ciphertext):
        """Generate cipher, decode, and decrypt data."""
        cipher = self._get_cipher()
        decoded_ciphertext = self._decode(ciphertext)
        plaintext = cipher.decrypt(decoded_ciphertext)
        return self.unpad(plaintext)

    def encrypt(self, plaintext):
        """Generate cipher, encrypt, and encode data."""
        cipher = self._get_cipher()
        padded_plaintext = self.pad(plaintext, self.cipher.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        return self._encode(ciphertext)

    def generate_iv(self):
        """Randomly generate an IV byte string of the object's block size.
        This has miniscule odds of producing a non-unique IV, which may be
        unsafe for OFB mode.
        """
        return Random.new().read(self.cipher.block_size)

    def pad(self, text, block_size):
        """Left pad text with a random character. Always add padding."""
        pad_char = self._get_pad_char(ignore=text[0])
        pad_size = (block_size - len(text)) % block_size or block_size
        return (pad_char * pad_size) + text

    def unpad(self, text):
        """Strip padding from text. It is expected that the `pad`
        method (or equivalent) has been applied.
        """
        return text.lstrip(text[0])
