
import os
import shutil

FILE_TARGETS = {'.txt', '.pdf', '.docx', '.jpg', '.png'}
COLLECTED_FOLDER = "collected_files"


def file_collector(copy_mode: bool = True):
    """Collects files with target extensions from Documents to a collected folder.

    Args:
        copy_mode (bool): If True, files are copied. If False, files are moved.
    """
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    os.makedirs(COLLECTED_FOLDER, exist_ok=True)

    for root, _, files in os.walk(documents_path):
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
