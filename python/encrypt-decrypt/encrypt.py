"""
encrypt_file.py

This script encrypts a file using a passphrase and saves the encrypted data as a base64 encoded hash to an output file.

Usage:
    python encrypt_file.py <input_file_path> <output_file_path> <passphrase>

Arguments:
    input_file_path    : Path to the input file to be encrypted.
    output_file_path   : Path to the output file where the encrypted data will be written.
    passphrase         : Passphrase used for encryption.

Example:
    python encrypt_file.py path/to/your/file.txt path/to/output/file.enc your_passphrase
"""

import sys
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def encrypt(data, passphrase):
    """
    Encrypts the given data using the provided passphrase.

    Args:
        data (bytes): The data to be encrypted.
        passphrase (str): The passphrase used to derive the encryption key.

    Returns:
        bytes: The base64 encoded encrypted data.
    """
    
    # Generate a random salt
    salt = os.urandom(16)

    # Derive a key from the passphrase using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the data to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Combine the salt, IV, and encrypted data
    encrypted_blob = salt + iv + encrypted_data

    # Base64 encode the encrypted blob
    encoded_data = base64.b64encode(encrypted_blob)

    return encoded_data

def main():
    if len(sys.argv) != 4:
        print("Usage: python encrypt_file.py <input_file_path> <output_file_path> <passphrase>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    passphrase = sys.argv[3]

    # Read the input file contents
    with open(input_file_path, 'rb') as file:
        file_data = file.read()

    # Encrypt and encode the file data
    encrypted_data = encrypt(file_data, passphrase)

    # Write the result to the output file
    with open(output_file_path, 'wb') as file:
        file.write(encrypted_data)

    print(f"Data successfully encrypted and written to {output_file_path}")

if __name__ == "__main__":
    main()