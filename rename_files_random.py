import os
import random
import string
from pathlib import Path


def generate_random_name(length=10):
    """Generate a random string of letters and digits."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def rename_files_recursively(directory: Path, name_length=10):
    """Recursively rename all files under the given directory."""
    for file_path in directory.iterdir():
        if file_path.is_file():
            new_name = generate_random_name(name_length) + file_path.suffix
            new_path = file_path.with_name(new_name)

            # Ensure unique filenames in the same directory
            while new_path.exists():
                new_name = generate_random_name(name_length) + file_path.suffix
                new_path = file_path.with_name(new_name)

            file_path.rename(new_path)
            print(f"✅ {file_path.relative_to(Path.cwd())} → {new_name}")

        elif file_path.is_dir():
            # Recurse into subdirectories
            rename_files_recursively(file_path, name_length)


def rename_files_in_current_directory(name_length=10):
    """Rename all files in the current working directory and subdirectories."""
    directory = Path.cwd()
    print(f"📂 Working recursively in: {directory}")
    rename_files_recursively(directory, name_length)


if __name__ == "__main__":
    rename_files_in_current_directory()
