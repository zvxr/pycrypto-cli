
import string

from crypto.classes.ciphers.base import CryptoCipher
from Crypto.Cipher import XOR
from Crypto import Random


class XORCipher(CryptoCipher):
    """Implements Pycrypto bitwise XOR stream cipher.
    Vulnerable to frequency analysis. Appropriate for hiding data, not securing it.
    """
    def __init__(self, key=None):
        super(XORCipher, self).__init__(key)

    @CryptoCipher.key.setter
    def key(self, value):
        if value is not None and len(value) not in XOR.key_size:
            raise AttributeError(
                "key must be {} - {} bytes long.".format(XOR.key_size[0], XOR.key_size[-1])
            )
        self._key = value

    def encrypt(self, plaintext):
        """Generate cipher, encrypt, and encode data."""
        xor_cipher = XOR.new(self.key)
        ciphertext = xor_cipher.encrypt(plaintext)
        return self._encode(ciphertext)

    def decrypt(self, ciphertext):
        """Generate cipher, decode, and decrypt data."""
        xor_cipher = XOR.new(self.key)
        decoded_ciphertext = self._decode(ciphertext)
        return xor_cipher.decrypt(decoded_ciphertext)


def generate_key(key_size=16, ascii_only=False):
    """Randomly generate a key of byte size `key_size`.
    Use only [a-z][A-Z] when `ascii_only` is True.
    """
    if key_size not in XOR.key_size:
        raise AttributeError(
            "key must be {} - {} bytes long.".format(XOR.key_size[0], XOR.key_size[-1])
        )

    if ascii_only:
        return "".join(Random.random.choice(string.ascii_letters) for i in xrange(key_size))
    else:
        random_device = Random.new()
        return random_device.read(key_size)
