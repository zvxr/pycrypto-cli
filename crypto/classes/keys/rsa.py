
from Crypto.PublicKey import RSA


def _generate_key(key_size):
    if not key_size % 256:
        raise AttributeError("key_size must be a multiple of 256.")
    if key_size < 1024:
        raise AttributeError("key_size must be at least 1024 bits.")

    return RSA.generate(key_size)


def generate_key(key_size=2048):
    """Generate a private key of bit size `key_size`.
    Must be a multiple of 256 and >= 1024 bytes.
    """
    key = _generate_key(key_size)

    return key.exportKey('PEM')


def generate_keys(key_size=2048):
    """Generate a public and private key set of bit size `key_size`.
    Must be a multiple of 256 and >= 1024 bytes.
    """
    key = _generate_key(key_size)
    public_key = key.publickey().exportKey('PEM')
    private_key = key.exportKey('PEM')

    return public_key, private_key


def import_key(key, passphrase=None):
    """Wraps pycrypto method for importing RSA key."""
    return RSA.importKey(key, passphrase=passphrase)
