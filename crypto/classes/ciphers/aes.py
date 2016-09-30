
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Counter


class AESCipher(BlockCipher):
    """AES symmetric cipher."""
    attributes = ('key', 'iv', 'mode')
    default_mode = AES.MODE_CFB
    supported_modes = {
        'CBC': AES.MODE_CBC,
        'CFB': AES.MODE_CFB,
        'CTR': AES.MODE_CTR,
        'ECB': AES.MODE_ECB,
        'OFB': AES.MODE_OFB
    }

    def __init__(self, key=None, iv=None, initial_value=1):
        """initial_value is only applied to CTR."""
        super(AESCipher, self).__init__(key, iv)
        self.initial_value = initial_value

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and len(value) not in (16, 24, 32):
            raise AttributeError(
                "key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long."
            )
        self._key = value

    @BlockCipher.iv.setter
    def iv(self, value):
        # Ignore IV for ECB mode.
        if self._mode == AES.MODE_ECB:
            return

        if value is not None and len(value) != AES.block_size:
            raise AttributeError(
                "iv must be {} bytes long.".format(AES.block_size)
            )
        self._iv = value

    def _get_counter(self):
        """Returns a stateful Counter instance of 128 bits to work
        with AES key sizes. No prefix or suffix is applied.
        """
        return Counter(128, initial_value=self.initial_value)

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

    def encrypt(self, plaintext):
        """Generate cipher, encrypt, and encode data."""
        aes_cipher = self._get_cipher()
        padded_plaintext = self.pad(plaintext, AES.block_size)
        ciphertext = aes_cipher.encrypt(padded_plaintext)
        return self._encode(ciphertext)

    def decrypt(self, ciphertext):
        """Generate cipher, decode, and decrypt data."""
        aes_cipher = self._get_cipher()
        decoded_ciphertext = self._decode(ciphertext)
        plaintext = aes_cipher.decrypt(decoded_ciphertext)
        return self.unpad(plaintext)

    def generate_iv(self):
        """Randomly generate an IV byte string for various modes of AES."""
        return Random.new().read(AES.block_size)

    def generate_key(self, key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be 16, 24, or 32."""
        if key_size not in (16, 24, 32):
            raise AttributeError(
                "key_size must be 16 (AES-128), 24 (AES-192), or 32 (AES-256)."
            )
        random_device = Random.new()
        return random_device.read(key_size)
