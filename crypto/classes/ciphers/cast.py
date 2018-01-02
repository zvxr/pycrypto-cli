from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import CAST


class CASTCipher(BlockCipher):
    """CAST-128 symmetric block cipher."""
    cipher = CAST

    def __init__(self, key=None, iv=None, mode=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(CASTCipher, self).__init__(key, iv, mode, initial_value)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and not (5 <= len(value) <= 16):
            raise AttributeError(
                "key must be between 5 and 16 bytes long."
            )
        self._key = value

    def generate_key(self, key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be between 5
        and 16.
        """
        if not 5 <= key_size <= 16:
            raise AttributeError(
                "key_size must be between 5 and 16 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
