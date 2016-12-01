
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import Blowfish


class BlowfishCipher(BlockCipher):
    """Blowfish symmetric block cipher."""
    attributes = ('key', 'iv', 'mode')
    block_size = Blowfish.block_size
    default_mode = Blowfish.MODE_ECB
    modes_ignore_iv = (Blowfish.MODE_CTR, Blowfish.MODE_ECB)
    modes_use_counter = (Blowfish.MODE_CTR,)
    supported_modes = {
        'CBC': Blowfish.MODE_CBC,
        'CFB': Blowfish.MODE_CFB,
        #'CTR': Blowfish.MODE_CTR,  # Does not work.
        'ECB': Blowfish.MODE_ECB,
        'OFB': Blowfish.MODE_OFB
    }

    def __init__(self, key=None, iv=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(BlowfishCipher, self).__init__(key, iv)
        self.initial_value = initial_value

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and not (4 <= len(value) <= 56):
            raise AttributeError(
                "key must be between 4 and 56 bytes long."
            )
        self._key = value

    @BlockCipher.iv.setter
    def iv(self, value):
        if self.ignore_iv:
            return

        if value is not None and len(value) != self.block_size:
            raise AttributeError(
                "iv must be {} bytes long.".format(self.block_size)
            )
        self._iv = value

    def _get_cipher(self):
        """Return a Pycrypto Blowfish cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self.use_counter:
            return Blowfish.new(self.key, self._mode, counter=self._get_counter())
        elif self.ignore_iv:
            return Blowfish.new(self.key, self._mode)
        else:
            return Blowfish.new(self.key, self._mode, self.iv)

    def generate_key(self, key_size=56):
        """Randomly generate a key of byte size `key_size`. Must be between 4 and 56."""
        if not 4 <= key_size <= 56:
            raise AttributeError(
                "key_size must be between 4 and 56 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
