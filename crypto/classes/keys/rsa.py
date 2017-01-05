
from Crypto.PublicKey import RSA


class RSAKeys(object):
    """Wraps Pycrypto RSA.
        key_size must be a multiple of 256 and >= 1024 bytes.
    """
    attributes = ('key',)
    supported_modes = ('DER', 'OpenSSH', 'PEM')

    def __init__(
        self,
        key_format,
        key_size,
        passphrase=None
    ):
        self.key_format = key_format
        self.key_size = key_size
        self.passphrase = passphrase
        self._key = None

    def __repr__(self):
        return "{} key {} set.".format(
            self.__class__,
            "is" if self._key is not None else "is not"
        )

    @property
    def key(self):
        """Lazy loads key when first accessed."""
        if self._key is None:
            self._key = self._generate_key()
        return self._key

    @property
    def key_format(self):
        return self._key_format

    @key_format.setter
    def key_format(self, value):
        if value not in self.supported_modes:
            raise AttributeError(
                "key_format does not match one of the supported modes: {}".format(self.supported_modes)
            )
        self._key_format = value

    @property
    def key_size(self):
        return self._key_size

    @key_size.setter
    def key_size(self, value):
        if value % 256 != 0:
            raise AttributeError("key_size must be a multiple of 256.")
        if value < 1024:
            raise AttributeError("key_size must be at least 1024 bits.")
        self._key_size = value

    def _generate_key(self):
        return RSA.generate(self.key_size)

    def get_private_key(self, passphrase=None):
        return self.key.exportKey(self.key_format, passphrase=passphrase)

    def get_public_key(self, passphrase=None):
        return self.key.publickey().exportKey(self.key_format, passphrase=passphrase)


def import_key(key, passphrase=None):
    """Wraps pycrypto method for importing RSA key."""
    return RSA.importKey(key, passphrase=passphrase)
