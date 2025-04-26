
import os
import shutil

COLLECTED_FOLDER = "collected_files"  
FILE_TARGETS = {'.txt', '.pdf', '.docx', '.jpg', '.png'}  

def file_collector(copy_mode: bool = True):
    """Collects files with target extensions from a user-specified folder to a collected folder.

    Args:
        copy_mode (bool): If True, files are copied. If False, files are moved.
    """
    print("\n📂🧭 Please provide the folder path to scan for files:")
    source_folder = input("📥 Path: ").strip()

    if not os.path.isdir(source_folder):
        print("❌ Invalid folder path. Exiting.")
        return

    os.makedirs(COLLECTED_FOLDER, exist_ok=True)

    for root, _, files in os.walk(source_folder):
        for file in files:
            if os.path.splitext(file)[1].lower() in FILE_TARGETS:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(COLLECTED_FOLDER, file)
                try:
                    if copy_mode:
                        shutil.copy2(src_path, dst_path)
                        print(f"📄 Copied: {src_path} -> {dst_path}")
                    else:
                        shutil.move(src_path, dst_path)
                        print(f"⇨ Moved: {src_path} -> {dst_path}")
                except PermissionError:
                    print(f"⛔ Access denied: {src_path}")

