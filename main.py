import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def copy_file(src_file: Path, dest_dir: Path):
    dest_file = dest_dir / src_file.name
    shutil.copy2(src_file, dest_file)

def process_directory(src_dir: Path, dest_dir: Path, executor: ThreadPoolExecutor):
    for entry in os.scandir(src_dir):
        if entry.is_file():
            ext = entry.name.split('.')[-1].lower()
            dest_subdir = dest_dir / ext
            dest_subdir.mkdir(parents=True, exist_ok=True)
            executor.submit(copy_file, Path(entry.path), dest_subdir)
        elif entry.is_dir():
            executor.submit(process_directory, Path(entry.path), dest_dir, executor)

def main(src_dir: str, dest_dir: str):
    src_path = Path(src_dir).resolve()
    dest_path = Path(dest_dir).resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        process_directory(src_path, dest_path, executor)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [destination_directory]")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"
    
    main(source_directory, destination_directory)
