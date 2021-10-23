from crypto.classes.ciphers.base import BlockCipher, BlockCipherMode
from Crypto import Random
from Crypto.Cipher import Blowfish


class BlowfishCipher(BlockCipher):
    """Blowfish symmetric block cipher."""
    cipher = Blowfish
    supported_modes = {
        'CBC': BlockCipherMode(Blowfish.MODE_CBC, True, False),
        'CFB': BlockCipherMode(Blowfish.MODE_CFB, True, False),
        'CTR': BlockCipherMode(Blowfish.MODE_CTR, False, True),
        'ECB': BlockCipherMode(Blowfish.MODE_ECB, False, False),
        'OFB': BlockCipherMode(Blowfish.MODE_OFB, True, False)
    }

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
        """Randomly generate a key of byte size `key_size`. Must be between 4
        and 56.
        """
        if not 4 <= key_size <= 56:
            raise AttributeError(
                "key_size must be between 4 and 56 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
