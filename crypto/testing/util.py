
import unittest

"""Utility (helper) methods for test suite.
"""


def test_cipher_encryption(testcase, cipher, plaintext):
    """This will execute a cipher's encrypt/decrypt methods and compare
    results. unittest assertions are made if `testcase` is a unittest.TestCase.
    Otherwise simple asserts are executed.
    """
    ciphertext = cipher.encrypt(plaintext)

    if isinstance(testcase, unittest.TestCase):
        testcase.assertTrue(ciphertext is not None)
        testcase.assertNotEqual(plaintext, ciphertext)
        testcase.assertEqual(plaintext, cipher.decrypt(ciphertext))
    else:
        assert ciphertext is not None
        assert plaintext != ciphertext
        assert plaintext == cipher.decrypt(ciphertext)
