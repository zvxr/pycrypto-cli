
import crypto.classes.ciphers.aes as aes_cipher
import crypto.classes.ciphers.base as base_cipher
import crypto.classes.ciphers.xor as xor_cipher
import crypto.classes.encoders.base as base_encoders
import crypto.classes.encoders.binary as binary_encoders
import mock
import string
import unittest
import util

from Crypto.Cipher import AES
from Crypto.Random import random


# Mixins for base classes.
class CryptoCipherMixin(object):
    """Mixin contains tests to be applied to anything that inherits from CryptoCipher
    base class. This test class must be inherited with unittest.TestCase to use.
    """
    def _test_init_no_args(self, cipher, overrides_encryption=True):
        self.assertEqual(cipher._key, None)
        self.assertEqual(cipher._encoder, None)
        self.assertEqual(cipher._decoder, None)
        self.assertRaises(AttributeError, getattr, cipher, 'key')

        if not overrides_encryption:
            self.assertRaises(NotImplementedError, cipher.encrypt, "meow")
            self.assertRaises(NotImplementedError, cipher.decrypt, "wruff")

    def _test_init_key(self, cipher, key_value):
        self.assertEqual(cipher._key, key_value)
        self.assertEqual(cipher.key, key_value)

    def _test_key_setter(self, cipher, valid_key, invalid_key=None):
        cipher.key = valid_key
        self.assertEqual(cipher._key, valid_key)
        self.assertEqual(cipher.key, valid_key)

        if invalid_key is not None:
            self.assertRaises(AttributeError, setattr, cipher, 'key', invalid_key)

    def _test_set_encoding(self, cipher):
        self.assertEqual(cipher._encode("meow", 32, paws_mode=True), "meow")
        self.assertEqual(cipher._decode("wruff", 57, tail_wag=True), "wruff")

        self.assertRaises(TypeError, cipher.set_encoding, lambda: None)
        encrypt = mock.Mock()
        decrypt = mock.Mock()
        encoder = base_encoders.Encoder(encrypt, decrypt)
        cipher.set_encoding(encoder)
        self.assertEqual(cipher._encode("meow", 32, paws_mode=True), encrypt.return_value)
        encrypt.assert_called_with("meow", 32, paws_mode=True)
        self.assertEqual(cipher._decode("wruff", 57, tail_wag=True), decrypt.return_value)
        decrypt.assert_called_with("wruff", 57, tail_wag=True)


class BlockCipherMixin(CryptoCipherMixin):
    """Mixin contains tests to be applied to anything that inherits from BlockCipher
    base class. This test class must be inherited with unittest.TestCase to use.
    """
    def _test_init_no_args(self, cipher, overrides_encryption=True):
        self.assertEqual(cipher._key, None)
        self.assertEqual(cipher._iv, None)
        self.assertEqual(cipher._encoder, None)
        self.assertEqual(cipher._decoder, None)
        self.assertRaises(AttributeError, getattr, cipher, 'key')

        if not overrides_encryption:
            self.assertRaises(NotImplementedError, cipher.encrypt, "meow")
            self.assertRaises(NotImplementedError, cipher.decrypt, "wruff")

    def _test_init_iv(self, cipher, iv_value):
        self.assertEqual(cipher._iv, iv_value)
        self.assertEqual(cipher.iv, iv_value)

    def _test_iv_setter(self, cipher, valid_iv, invalid_iv=None):
        cipher.iv = valid_iv
        self.assertEqual(cipher._iv, valid_iv)
        self.assertEqual(cipher.iv, valid_iv)

        if invalid_iv is not None:
            self.assertRaises(AttributeError, setattr, cipher, 'iv', invalid_iv)

    @mock.patch('Crypto.Random.new')
    def _test_get_pad_char(self, cipher, random_new_mock):
        random_device_mock = mock.Mock()
        random_new_mock.return_value = random_device_mock

        random_device_mock.read.side_effect = ["m", "e", "o", "w"]
        self.assertEqual(cipher._get_pad_char(), "m")
        random_device_mock.read.assert_called_with(1)

        self.assertEqual(cipher._get_pad_char(ignore="e"), "o")
        self.assertEqual(cipher._get_pad_char(ignore="m"), "w")

    @mock.patch('crypto.classes.ciphers.base.BlockCipher._get_pad_char')
    def _test_pad(self, cipher, get_pad_char_mock):
        get_pad_char_mock.return_value = "_"
        self.assertEqual(cipher.pad("meow", 6), "__meow")
        get_pad_char_mock.assert_called_with(ignore="m")

        self.assertEqual(cipher.pad("meow", 4), "____meow")
        self.assertEqual(cipher.pad("meow", 2), "__meow")

    def _test_unpad(self, cipher):
        self.assertEqual(cipher.unpad("____meow"), "meow")
        self.assertEqual(cipher.unpad("__meow"), "meow")
        self.assertEqual(cipher.unpad("meow"), "eow")


# Tests for base classes.
class CryptoCipherTest(unittest.TestCase, CryptoCipherMixin):
    def test_init(self):
        cipher = base_cipher.CryptoCipher()
        self._test_init_no_args(cipher, overrides_encryption=False)

    def test_key_property(self):
        cipher = base_cipher.CryptoCipher(key="fishsticks")
        self._test_init_key(cipher, "fishsticks")
        self._test_key_setter(cipher, "puppychow")

    def test_set_encoding(self):
        cipher = base_cipher.CryptoCipher()
        self._test_set_encoding(cipher)


class BlockCipherTest(unittest.TestCase, BlockCipherMixin):
    def test_init(self):
        cipher = base_cipher.BlockCipher()
        self._test_init_no_args(cipher, overrides_encryption=True)

    def test_init_args(self):
        cipher = base_cipher.BlockCipher(key="fishsticks", iv="meow", mode='CBC')
        self._test_init_key(cipher, "fishsticks")
        self._test_init_iv(cipher, "meow")

    def test_iv_property(self):
        cipher = base_cipher.BlockCipher(iv="meow", mode='CBC')
        self._test_init_iv(cipher, "meow")
        self._test_iv_setter(cipher, "")

    def test_get_pad_char(self):
        cipher = base_cipher.BlockCipher()
        self._test_get_pad_char(cipher)

    def test_pad(self):
        cipher = base_cipher.BlockCipher()
        self._test_pad(cipher)

    def test_unpad(self):
        cipher = base_cipher.BlockCipher()
        self._test_unpad(cipher)


# Tests for implemented cipher classes.
class AESCipherTest(unittest.TestCase, BlockCipherMixin):
    def test_init(self):
        cipher = aes_cipher.AESCipher()
        self._test_init_no_args(cipher)

    def test_key_property(self):
        cipher = aes_cipher.AESCipher(key="wruff wruff meow")
        self._test_init_key(cipher, "wruff wruff meow")
        self._test_key_setter(cipher, "meow wruff wruff", invalid_key="wruff")

    def test_iv_property(self):
        cipher = aes_cipher.AESCipher(iv="meow wruff wruff", mode='CBC')
        self._test_init_iv(cipher, "meow wruff wruff")
        self._test_iv_setter(cipher, "wruff wruff meow", invalid_iv="wruff")

    def test_mode_property(self):
        cipher = aes_cipher.AESCipher()  # Expects Cipher FeedBack.
        self.assertEqual(cipher._mode.mode_id, AES.MODE_ECB)

        cipher.mode = 'CTR'
        self.assertEqual(cipher._mode.mode_id, AES.MODE_CTR)

    def test_generate_iv(self):
        cipher = aes_cipher.AESCipher()
        self.assertEqual(len(cipher.generate_iv()), AES.block_size)

    def test_generate_key(self):
        cipher = aes_cipher.AESCipher()
        self.assertEqual(len(cipher.generate_key()), 16)  # test default.
        self.assertEqual(len(cipher.generate_key(16)), 16)
        self.assertEqual(len(cipher.generate_key(24)), 24)
        self.assertEqual(len(cipher.generate_key(32)), 32)
        self.assertRaises(AttributeError, cipher.generate_key, 48)

    def test_set_encoding(self):
        cipher = aes_cipher.AESCipher()
        self._test_set_encoding(cipher)

    @mock.patch('Crypto.Cipher.AES.new')
    def test_get_cipher(self, aes_new_mock):
        cipher = aes_cipher.AESCipher(
            key="wruff wruff meow",
            iv="meow wruff wruff"
        )
        cipher.mode = 'CFB'
        self.assertEqual(cipher._get_cipher(), aes_new_mock.return_value)
        aes_new_mock.assert_called_with("wruff wruff meow", AES.MODE_CFB, "meow wruff wruff")

        cipher = aes_cipher.AESCipher(
            key="wruff wruff meow",
            iv="meow wruff wruff"
        )
        cipher.mode = 'ECB'
        self.assertEqual(cipher._get_cipher(), aes_new_mock.return_value)
        aes_new_mock.assert_called_with("wruff wruff meow", AES.MODE_ECB)

    @mock.patch('crypto.classes.ciphers.aes.AESCipher._encode')
    @mock.patch('crypto.classes.ciphers.aes.AESCipher.pad')
    @mock.patch('crypto.classes.ciphers.aes.AESCipher._get_cipher')
    def test_encrypt(self, get_cipher_mock, pad_mock, encode_mock):
        aes_cipher_mock = get_cipher_mock.return_value
        cipher = aes_cipher.AESCipher()
        self.assertEqual(cipher.encrypt("meow"), encode_mock.return_value)
        get_cipher_mock.assert_called_with()
        pad_mock.assert_called_with("meow", AES.block_size)
        aes_cipher_mock.encrypt.assert_called_with(pad_mock.return_value)
        encode_mock.assert_called_with(aes_cipher_mock.encrypt.return_value)

    @mock.patch('crypto.classes.ciphers.aes.AESCipher._decode')
    @mock.patch('crypto.classes.ciphers.aes.AESCipher.unpad')
    @mock.patch('crypto.classes.ciphers.aes.AESCipher._get_cipher')
    def test_decrypt(self, get_cipher_mock, unpad_mock, decode_mock):
        aes_cipher_mock = get_cipher_mock.return_value
        cipher = aes_cipher.AESCipher()
        self.assertEqual(cipher.decrypt("wruff"), unpad_mock.return_value)
        get_cipher_mock.assert_called_with()
        decode_mock.assert_called_with("wruff")
        aes_cipher_mock.decrypt.assert_called_with(decode_mock.return_value)
        unpad_mock.assert_called_with(aes_cipher_mock.decrypt.return_value)

    def test_encryption_cbc(self):
        """This will actually execute encrypting/decrypting data for CBC mode."""
        self._test_encryption('CBC')

    def test_encryption_cfb(self):
        """This will actually execute encrypting/decrypting data for CFB mode."""
        self._test_encryption('CFB')

    def test_encryption_ecb(self):
        """This will actually execute encrypting/decrypting data for ECB mode."""
        self._test_encryption('ECB')

    def test_encryption_ofb(self):
        """This will actually execute encrypting/decrypting data for OFB mode."""
        self._test_encryption('OFB')

    def _test_encryption(self, mode):
        """This will actually execute encrypting/decrypting data.
        Key and IV generation is derived entirely from class staticmethods.
        """
        cipher = aes_cipher.AESCipher()
        cipher.mode = mode
        cipher.iv = cipher.generate_iv()
        random_device = random.Random.new()

        # Test various key sizes.
        for key_size in (16, 24, 32):
            cipher.key = cipher.generate_key(key_size)
            util.test_cipher_encryption(self, cipher, random_device.read(2000))

        # Test encoders.
        for encoder in (
            base_encoders.NullEncoder,
            binary_encoders.Base64Encoder,
            binary_encoders.URLSafeBase64Encoder
        ):
            cipher.set_encoding(encoder)
            util.test_cipher_encryption(self, cipher, random_device.read(2000))


class XORCipherTest(unittest.TestCase, CryptoCipherMixin):
    def test_init(self):
        cipher = xor_cipher.XORCipher()
        self._test_init_no_args(cipher)

    def test_key_property(self):
        cipher = xor_cipher.XORCipher(key="fishsticks")
        self._test_init_key(cipher, "fishsticks")
        self._test_key_setter(cipher, "puppychow", invalid_key="puppy" * 12)

    def test_set_encoding(self):
        cipher = xor_cipher.XORCipher()
        self._test_set_encoding(cipher)

    @mock.patch('crypto.classes.ciphers.xor.XORCipher._encode')
    @mock.patch('Crypto.Cipher.XOR.new')
    def test_encrypt(self, xor_new_mock, encode_mock):
        xor_cipher_mock = xor_new_mock.return_value
        cipher = xor_cipher.XORCipher("fishsticks")
        self.assertEqual(cipher.encrypt("meow"), encode_mock.return_value)
        xor_new_mock.assert_called_with("fishsticks")
        xor_cipher_mock.encrypt.assert_called_with("meow")
        encode_mock.assert_called_with(xor_cipher_mock.encrypt.return_value)

    @mock.patch('crypto.classes.ciphers.xor.XORCipher._decode')
    @mock.patch('Crypto.Cipher.XOR.new')
    def test_decrypt(self, xor_new_mock, decode_mock):
        xor_cipher_mock = xor_new_mock.return_value
        cipher = xor_cipher.XORCipher("puppychow")
        self.assertEqual(cipher.decrypt("wruff"), xor_cipher_mock.decrypt.return_value)
        xor_new_mock.assert_called_with("puppychow")
        decode_mock.assert_called_with("wruff")
        xor_cipher_mock.decrypt.assert_called_with(decode_mock.return_value)

    def test_generate_key(self):
        # Test random byte array.
        cipher = xor_cipher.XORCipher()
        self.assertEqual(len(cipher.generate_key()), 16)  # test default.
        self.assertEqual(len(cipher.generate_key(16)), 16)
        self.assertEqual(len(cipher.generate_key(32)), 32)
        self.assertRaises(AttributeError, cipher.generate_key, 48)

        # Test ASCII only.
        self.assertEqual(len(cipher.generate_key(ascii_only=True)), 16)
        for char in cipher.generate_key(32, ascii_only=True):
            self.assertTrue(char in string.ascii_letters)

    def test_encryption(self):
        """This will actually execute encrypting/decrypting data."""
        cipher = xor_cipher.XORCipher("fishsticks")

        def run(cipher, plaintext):
            ciphertext = cipher.encrypt(plaintext)
            self.assertTrue(ciphertext is not None)
            self.assertNotEqual(plaintext, ciphertext)
            self.assertEqual(plaintext, cipher.decrypt(ciphertext))

        # Test string/byte array.
        util.test_cipher_encryption(self, cipher, "meow" * 500)
        util.test_cipher_encryption(self, cipher, random.Random.new().read(2000))

        # Test encoders.
        cipher.set_encoding(base_encoders.NullEncoder)
        util.test_cipher_encryption(self, cipher, "wruff" * 400)
        util.test_cipher_encryption(self, cipher, random.Random.new().read(2000))

        cipher.set_encoding(binary_encoders.Base64Encoder)
        util.test_cipher_encryption(self, cipher, "meow" * 500)
        util.test_cipher_encryption(self, cipher, random.Random.new().read(2000))

        cipher.set_encoding(binary_encoders.URLSafeBase64Encoder)
        util.test_cipher_encryption(self, cipher, "wruff" * 400)
        util.test_cipher_encryption(self, cipher, random.Random.new().read(2000))

        # Test keys and instances.
        cipher1 = xor_cipher.XORCipher("fishsticks")
        cipher2 = xor_cipher.XORCipher("fishsticks")
        cipher3 = xor_cipher.XORCipher("puppychow")

        self.assertEqual(cipher1.encrypt("meow"), cipher2.encrypt("meow"))
        self.assertNotEqual(cipher2.encrypt("wruff"), cipher3.encrypt("wruff"))


if __name__ == "__main__":
    unittest.main()
