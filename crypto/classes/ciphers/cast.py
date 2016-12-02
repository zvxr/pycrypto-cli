
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import CAST


class CASTCipher(BlockCipher):
    """CAST-128 symmetric block cipher."""
    attributes = ('key', 'iv', 'mode')
    block_size = CAST.block_size
    default_mode = CAST.MODE_ECB
    modes_ignore_iv = (CAST.MODE_CTR, CAST.MODE_ECB)
    modes_use_counter = (CAST.MODE_CTR,)
    supported_modes = {
        'CBC': CAST.MODE_CBC,
        'CFB': CAST.MODE_CFB,
        'CTR': CAST.MODE_CTR,
        'ECB': CAST.MODE_ECB,
        'OFB': CAST.MODE_OFB
    }

    def __init__(self, key=None, iv=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(CASTCipher, self).__init__(key, iv, initial_value)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and not (5 <= len(value) <= 16):
            raise AttributeError(
                "key must be between 5 and 16 bytes long."
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
        """Return a Pycrypto CAST-128 cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self.use_counter:
            return CAST.new(self.key, self._mode, counter=self._get_counter())
        elif self.ignore_iv:
            return CAST.new(self.key, self._mode)
        else:
            return CAST.new(self.key, self._mode, self.iv)

    def generate_key(self, key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be between 5 and 16."""
        if not 5 <= key_size <= 16:
            raise AttributeError(
                "key_size must be between 5 and 16 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
