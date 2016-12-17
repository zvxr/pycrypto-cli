
from Crypto.PublicKey import RSA


_SUPPORTED_KEY_FORMATS = ('DER', 'OpenSSH', 'PEM')


def _generate_key(key_size):
    if key_size % 256:
        raise AttributeError("key_size must be a multiple of 256.")
    if key_size < 1024:
        raise AttributeError("key_size must be at least 1024 bits.")

    return RSA.generate(key_size)


def _validate_key_format(key_format):
    if key_format not in _SUPPORTED_KEY_FORMATS:
        raise AttributeError(
            "Unknown value for key_format. Must be {}".format(_SUPPORTED_KEY_FORMATS)
        )


def generate_key_pair(key_size=2048, key_format='PEM'):
    """Generate a public/private key set of bit size `key_size` using format `key_format`.
    `key_size` must be a multiple of 256 and >= 1024 bytes.
    `key_format` must be 'PEM', 'DER', or 'OpenSSH'.
    """
    _validate_key_format(key_format)
    key = _generate_key(key_size)
    public_key = key.publickey().exportKey(key_format)
    private_key = key.exportKey(key_format)

    return public_key, private_key


def generate_private_key(key_format='PEM', key_size=2048):
    """Generate a private key of bit size `key_size` using format `key_format`.
    `key_size` must be a multiple of 256 and >= 1024 bytes.
    `key_format` must be 'PEM', 'DER', or 'OpenSSH'.
    """
    _validate_key_format(key_format)
    key = _generate_key(key_size)

    return key.exportKey(key_format)


def generate_public_key(key_format='PEM', key_size=2048):
    """Generate a public key of bit size `key_size` using format `key_format`.
    `key_size` must be a multiple of 256 and >= 1024 bytes.
    `key_format` must be 'PEM', 'DER', or 'OpenSSH'.
    """
    _validate_key_format(key_format)
    key = _generate_key(key_size)

    return key.publickey().exportKey(key_format)


def import_key(key, passphrase=None):
    """Wraps pycrypto method for importing RSA key."""
    return RSA.importKey(key, passphrase=passphrase)
