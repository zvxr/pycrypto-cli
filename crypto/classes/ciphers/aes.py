
from crypto.classes.ciphers.base import BlockCipher
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(BlockCipher):
    """AES symmetric cipher."""
    SUPPORTED_MODES = (
        AES.MODE_CBC,
        AES.MODE_CFB,
        AES.MODE_ECB,
        AES.MODE_OFB
    )

    def __init__(self, key=None, iv=None, mode=AES.MODE_CFB):
        super(AESCipher, self).__init__(key, iv)
        self._mode = mode

    @staticmethod
    def generate_iv():
        """Randomly generate an IV byte string for various modes of AES."""
        return Random.new().read(AES.block_size)

    @staticmethod
    def generate_key(key_size=16):
        """Randomly generate a key of byte size `key_size`. Must be 16, 24, or 32."""
        if key_size not in (16, 24, 32):
            raise AttributeError(
                "key_size must be 16 (AES-128), 24 (AES-192), or 32 (AES-256)."
            )
        random_device = Random.new()
        return random_device.read(key_size)

    @BlockCipher.key.setter
    def key(self, value):
        if value is not None and len(value) not in (16, 24, 32):
            raise AttributeError(
                "key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long."
            )
        self._key = value

    @BlockCipher.iv.setter
    def iv(self, value):
        if value is not None and len(value) != AES.block_size:
            raise AttributeError(
                "iv must be {} bytes long.".format(AES.block_size)
            )
        self._iv = value

    @property
    def mode(self):
        if self._mode is not None:
            return self._mode
        raise AttributeError("Mode is not set.")

    @mode.setter
    def mode(self, value):
        if value not in AESCipher.SUPPORTED_MODES:
            raise AttributeError("AES mode not supported.")
        self._mode = value

    def _get_cipher(self):
        """Return a Pycrypto AES cipher instance.
        `key`, `mode` and depending on mode `iv` must be set.
        """
        if self.mode in (AES.MODE_ECB, AES.MODE_CTR):
            return AES.new(self.key, self.mode)
        return AES.new(self.key, self.mode, self.iv)

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
