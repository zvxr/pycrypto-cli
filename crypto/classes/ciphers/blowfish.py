
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import Blowfish


class BlowfishCipher(BlockCipher):
    """Blowfish symmetric block cipher."""
    attributes = ('key', 'iv', 'mode')
    default_mode = Blowfish.MODE_ECB
    supported_modes = {
        'CBC': Blowfish.MODE_CBC,
        'CFB': Blowfish.MODE_CFB,
        'CTR': Blowfish.MODE_CTR,
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
        # Ignore IV for ECB mode.
        if self._mode == Blowfish.MODE_ECB:
            return

        if value is not None and len(value) != Blowfish.block_size:
            raise AttributeError(
                "iv must be {} bytes long.".format(Blowfish.block_size)
            )
        self._iv = value

    def _get_cipher(self):
        """Return a Pycrypto Blowfish cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self._mode == Blowfish.MODE_ECB:
            return Blowfish.new(self.key, self._mode)
        elif self._mode == Blowfish.MODE_CTR:
            return Blowfish.new(self.key, self._mode, counter=self._get_counter())
        else:
            return Blowfish.new(self.key, self._mode, self.iv)

    def encrypt(self, plaintext):
        """Generate cipher, encrypt, and encode data."""
        blowfish_cipher = self._get_cipher()
        padded_plaintext = self.pad(plaintext, Blowfish.block_size)
        ciphertext = blowfish_cipher.encrypt(padded_plaintext)
        return self._encode(ciphertext)

    def decrypt(self, ciphertext):
        """Generate cipher, decode, and decrypt data."""
        blowfish_cipher = self._get_cipher()
        decoded_ciphertext = self._decode(ciphertext)
        plaintext = blowfish_cipher.decrypt(decoded_ciphertext)
        return self.unpad(plaintext)

    def generate_iv(self):
        """Randomly generate an IV byte string for various modes of Blowfish."""
        return Random.new().read(Blowfish.block_size)

    def generate_key(self, key_size=56):
        """Randomly generate a key of byte size `key_size`. Must be between 4 and 56."""
        if not 4 <= key_size <= 56:
            raise AttributeError(
                "key_size must be between 4 and 56 bytes."
            )
        random_device = Random.new()
        return random_device.read(key_size)
