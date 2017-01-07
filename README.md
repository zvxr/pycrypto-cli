# pycrypto-cli

A command-line interface that wraps Pycrypto. Allows for quick and easy
implementation of Ciphers and Hashes.

```
$ python cli.py -h
usage: pycrypto-cli [-h] {cipher,hash} ...

positional arguments:
  {cipher,hash}  Pycrypto module to use.
    cipher       Use cipher module.
    hash         Use hash module.

optional arguments:
  -h, --help     show this help message and exit


$ python cli.py cipher -h
usage: pycrypto-cli cipher [-h] [--clipboard] [--input DATA_INPUT_PATH]
                           [--output DATA_OUTPUT_PATH] [--decrypt]
                           [--encoder {URLSAFEBASE64,BASE64,NULL}]
                           [--iv IV_PATH] [--iv-gen] [--key KEY_PATH]
                           [--key-gen] [--mode {OFB,CBC,CFB,ECB,CTR}]
                           {CAST,AES,XOR,BLOWFISH}

positional arguments:
  {CAST,AES,XOR,BLOWFISH}
                        Cipher algorithm to apply.

optional arguments:
  -h, --help            show this help message and exit
  --clipboard, -c       Data is pulled from and stored in clipboard.
  --input DATA_INPUT_PATH, -i DATA_INPUT_PATH
                        Path to data to manipulate.
  --output DATA_OUTPUT_PATH, -o DATA_OUTPUT_PATH
                        Path to file to write data out to.
  --decrypt, -d         When True will decrypt data. When False will encrypt
                        data.
  --encoder {URLSAFEBASE64,BASE64,NULL}, -e {URLSAFEBASE64,BASE64,NULL}
                        Encoder/Decoder to apply to text when
                        encrypting/decrypting.
  --iv IV_PATH, -iv IV_PATH
                        Path to initialization vector used to encrypt or
                        decrypt. IV must adhere to constraints of cipher.
  --iv-gen, -IV         Generate a random IV automatically.
  --key KEY_PATH, -k KEY_PATH
                        Path to key used to encrypt or decrypt. Key size must
                        adhere to constraints of cipher.
  --key-gen, -K         Generate a random key automatically.
  --mode {OFB,CBC,CFB,ECB,CTR}, -m {OFB,CBC,CFB,ECB,CTR}
                        Chaining mode to use. This applies only to block
                        ciphers.

```


## Usage

```
$ python cli.py cipher xor
Please type data. Press ENTER twice or CTRL+C to end.
helloworld

Please enter a valid key: password
DATA: GAQfHxgYHRYcBQ==

$ python cli.py cipher xor -d
Please type data. Press ENTER twice or CTRL+C to end.
GAQfHxgYHRYcBQ==

Please enter a valid key: password
DATA: helloworld
```


## Testing

Executing unit tests:
```
python -m crypto.testing.cipher_tests
```
