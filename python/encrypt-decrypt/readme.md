# Encrypt and Decrypt

- [decrypt.py](decrypt.py) - This script takes an input file, a target output file and a passphrase and decrypts in input file using the passkey and saves the decrypted output to the output file.  Note, the input is assumed to be the SHA256 Hash in a BASE64 encoded format.  The output is the output.  LOL
- [encrypt.py](./encrypt.py) - This script is the opposite of the descrupt.py file.  It too takes an input file, a target output file and a passphrase.  It makes NO assumptions of the input file data, it uses the SHA256 HASH algorithm and the passkey to encrypt then BASE64 encode the encrypted data and save it to the output file.  Thus, the output file is assumed to be base64 encoded.
