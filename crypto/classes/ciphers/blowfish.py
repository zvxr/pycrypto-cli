
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import Blowfish


class BlowfishCipher(BlockCipher):
    """Blowfish symmetric block cipher."""
    cipher = Blowfish

    def __init__(self, key=None, iv=None, mode=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(BlowfishCipher, self).__init__(key, iv, mode, initial_value)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and not (4 <= len(value) <= 56):
            raise AttributeError(
                "key must be between 4 and 56 bytes long."
            )
        self._key = value

    def generate_key(self, key_size=56):
        """Randomly generate a key of byte size `key_size`. Must be between 4 and 56."""
        if not 4 <= key_size <= 56:
            raise AttributeError(
                "key_size must be between 4 and 56 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
