import zipfile
import os

def create_archive(archive_name, paths):
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in paths:
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(path)))
            else:
                zipf.write(path, os.path.basename(path))
    return archive_name

def extract_archive(archive_name, extract_path):
    with zipfile.ZipFile(archive_name, 'r') as zipf:
        zipf.extractall(extract_path)
def get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size

def get_archive_size_and_compression(archive_name, paths):
    original_size = sum(get_size(path) for path in paths)
    compressed_size = os.path.getsize(archive_name)
    return original_size, compressed_size

