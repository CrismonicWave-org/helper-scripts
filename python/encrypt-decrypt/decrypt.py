"""
decrypt_file.py

This script decrypts a base64 encoded encrypted file using a passphrase and saves the clear 
text to an output file.

Usage:
    python decrypt_file.py <input_file_path> <output_file_path> <passphrase>

Arguments:
    input_file_path    : Path to the input file containing base64 encoded encrypted data.
    output_file_path   : Path to the output file where the decrypted clear text will be written.
    passphrase         : Passphrase used for decryption.

Example:
    python decrypt_file.py path/to/your/encrypted_file.enc path/to/output/file.txt your_passphrase
"""

import sys
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def decrypt(encoded_data, passphrase):
    # Base64 decode the encrypted blob
    encrypted_blob = base64.b64decode(encoded_data)

    # Extract the salt, IV, and encrypted data
    salt = encrypted_blob[:16]
    iv = encrypted_blob[16:32]
    encrypted_data = encrypted_blob[32:]

    # Derive the key from the passphrase using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())

    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data

def main():
    if len(sys.argv) != 4:
        print("Usage: python decrypt_file.py <input_file_path> <output_file_path> <passphrase>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    passphrase = sys.argv[3]

    # Read the input file contents
    with open(input_file_path, 'rb') as file:
        encoded_data = file.read()

    # Decode and decrypt the file data
    decrypted_data = decrypt(encoded_data, passphrase)

    # Write the result to the output file
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)

    print(f"Data successfully decrypted and written to {output_file_path}")

if __name__ == "__main__":
    main()
