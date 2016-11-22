
from crypto.classes.encoders.base import Encoder
from Crypto import Random
from Crypto.Util import Counter


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
    attributes = ('key', 'iv')
    block_size = 0
    default_mode = None
    modes_ignore_iv = ()
    modes_use_counter = ()
    supported_modes = {}

    def __init__(self, key=None, iv=None, initial_value=1):
        super(BlockCipher, self).__init__(key)
        self._mode = self.default_mode
        self._iv = iv
        self.initial_value = initial_value

    def __repr__(self):
        return "{} key {} set, IV {} set.".format(
            self.__class__,
            "is" if self._key is not None else "is not",
            "is" if self._iv is not None else "is not"
        )

    @property
    def ignore_iv(self):
        """This will return a Boolean on if the IV when getting or setting should
        be ignored.
        """
        return self.mode in self.modes_ignore_iv

    @property
    def iv(self):
        if self.ignore_iv:
            return

        if self._iv is not None:
            return self._iv

        raise AttributeError("IV is not set.")

    @iv.setter
    def iv(self, value):
        if self.ignore_iv:
            return

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

    @property
    def use_counter(self):
        """This will return a Boolean on if a counter is necessary (based on mode).
        """
        return self.mode in self.modes_use_counter

    def _get_counter(self):
        """Returns a stateful Counter instance of 128 bits.
        No prefix or suffix is applied.
        """
        return Counter(128, initial_value=self.initial_value)

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
        padded_plaintext = self.pad(plaintext, self.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        return self._encode(ciphertext)

    def generate_iv(self):
        """Randomly generate an IV byte string of the object's block size."""
        return Random.new().read(self.block_size)

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
