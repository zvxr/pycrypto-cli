from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(BlockCipher):
    """AES symmetric cipher."""
    cipher = AES

    def __init__(self, key=None, iv=None, mode=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(AESCipher, self).__init__(key, iv, mode, initial_value)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and len(value) not in (16, 24, 32):
            raise AttributeError(
                (
                    "key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) " +
                    "bytes long."
                )
            )
        self._key = value

    def generate_key(self, key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be 16, 24, or
        32."""
        if key_size not in (16, 24, 32):
            raise AttributeError(
                "key_size must be 16 (AES-128), 24 (AES-192), or 32 (AES-256)."
            )
        random_device = Random.new()
        return random_device.read(key_size)
