
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(BlockCipher):
    """AES symmetric cipher."""
    attributes = ('key', 'iv', 'mode')
    block_size = AES.block_size
    default_mode = AES.MODE_CFB
    modes_ignore_iv = (AES.MODE_ECB,)
    supported_modes = {
        'CBC': AES.MODE_CBC,
        'CFB': AES.MODE_CFB,
        'CTR': AES.MODE_CTR,
        'ECB': AES.MODE_ECB,
        'OFB': AES.MODE_OFB
    }

    def __init__(self, key=None, iv=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(AESCipher, self).__init__(key, iv, initial_value)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and len(value) not in (16, 24, 32):
            raise AttributeError(
                "key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long."
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
        """Return a Pycrypto AES cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self._mode == AES.MODE_ECB:
            return AES.new(self.key, self._mode)
        elif self._mode == AES.MODE_CTR:
            return AES.new(self.key, self._mode, counter=self._get_counter())
        else:
            return AES.new(self.key, self._mode, self.iv)

    def generate_key(self, key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be 16, 24, or 32."""
        if key_size not in (16, 24, 32):
            raise AttributeError(
                "key_size must be 16 (AES-128), 24 (AES-192), or 32 (AES-256)."
            )
        random_device = Random.new()
        return random_device.read(key_size)
