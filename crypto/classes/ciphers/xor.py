import random
import string

from crypto.classes.ciphers.base import CryptoCipher
#from crypto.ports.xor import XOR
from Crypto.Util import strxor
from mock import Mock; XOR = Mock()
from Crypto import Random


class XORCipher(CryptoCipher):
    """Implements Pycrypto bitwise XOR stream cipher. Vulnerable to frequency
    analysis. Appropriate for hiding data, not securing it.
    """
    attributes = ('key',)

    def __init__(self, key=None):
        super(XORCipher, self).__init__(key)

    @CryptoCipher.key.setter
    def key(self, value):
        #if value is not None and len(value) not in XOR.key_size:
        #    raise AttributeError(
        #        "key must be %s - %s bytes long." % (
        #            XOR.key_size[0],
        #            XOR.key_size[-1]
        #        )
        #    )
        self._key = bytes(value, 'utf-8')

    def encrypt(self, plaintext):
        """Generate cipher, encrypt, and encode data."""
        #xor_cipher = XOR.new(self.key)
        #ciphertext = xor_cipher.encrypt(plaintext)
        ciphertext = strxor.strxor(self.key, bytes(plaintext, 'utf-8'))
        return self._encode(ciphertext)

    def decrypt(self, ciphertext):
        """Generate cipher, decode, and decrypt data."""
        #xor_cipher = XOR.new(self.key)
        decoded_ciphertext = self._decode(ciphertext)
        #return xor_cipher.decrypt(decoded_ciphertext)
        key = self.key * (len(decoded_ciphertext) // len(self.key))
        if len(decoded_ciphertext) % len(self.key):
            key += self.key[:len(decoded_ciphertext) % len(self.key)]
        return strxor.strxor(key, decoded_ciphertext)

    def generate_key(self, key_size=16, ascii_only=True):
        """Randomly generate a key of byte size `key_size`.
        Use only [a-z][A-Z] when `ascii_only` is True.
        """
        #if key_size not in XOR.key_size:
        #    raise AttributeError(
        #        "key must be %s - %s bytes long." % (
        #            XOR.key_size[0],
        #            XOR.key_size[-1]
        #        )
        #    )

        if ascii_only:
            return "".join(
                random.choice(string.ascii_letters) for i in xrange(key_size)
            )
        else:
            random_device = Random.new()
            return random_device.read(key_size)
