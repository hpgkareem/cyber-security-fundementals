
import os
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend

# Constants
DOCX = os.path.join(os.path.expanduser("~"), "Documents")
DECRYPTED_ZIP_FILE = os.path.join(DOCX, "decrypted_archive.zip")
RESTORE_FOLDER = os.path.join(DOCX, "restored_files")


def file_decryptor(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypts ciphertext using AES-CBC with PKCS7 unpadding."""
    iv, ct = ciphertext[:16], ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ct) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext


def Archive_decryptor(enc_path: str, key_hex: str):
    """Decrypts an encrypted archive and extracts its contents to RESTORE_FOLDER."""
    key = bytes.fromhex(key_hex)

    with open(enc_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()

    decrypted_zip = file_decryptor(encrypted_data, key)

    # Save the decrypted ZIP file
    with open(DECRYPTED_ZIP_FILE, 'wb') as zip_file:
        zip_file.write(decrypted_zip)

    # Ensure the restore folder exists
    os.makedirs(RESTORE_FOLDER, exist_ok=True)

    # Extract the ZIP contents
    with zipfile.ZipFile(DECRYPTED_ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(RESTORE_FOLDER)

    print(f"file has been decrypted successfully and saved to: {RESTORE_FOLDER}")
