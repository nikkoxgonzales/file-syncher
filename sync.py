import json
import os
import shutil

CONFIG_FILE = "config.json"
FILES_TXT = "files.txt"


def load_config():
    """Load configuration from config.json."""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def get_files_txt_path(destination):
    """Return the path to files.txt on the USB root."""
    return os.path.join(destination, FILES_TXT)


def read_files_txt(files_txt_path):
    """Read files.txt and return a set of file paths."""
    if not os.path.exists(files_txt_path):
        return set()
    with open(files_txt_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def write_files_txt(files_txt_path, files):
    """Write the set of file paths to files.txt."""
    with open(files_txt_path, "w", encoding="utf-8") as f:
        for file in sorted(files):
            f.write(f"{file}\n")


def list_source_files(source, ignored_extensions):
    """List all files in source, ignoring specified extensions."""
    files = set()
    for root, _, filenames in os.walk(source):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in ignored_extensions):
                continue
            rel_path = os.path.relpath(os.path.join(root, filename), source)
            files.add(rel_path.replace("\\", "/"))
    return files


def sync_files(config):
    """Synchronize files between source and destination."""
    source = config["source"]
    destination = config["destination"]
    ignored_extensions = config.get("ignored_extensions", [])

    files_txt_path = get_files_txt_path(destination)
    print(f'Source: "{source}"')
    print(f'Destination: "{destination}"')
    print(f'files.txt path: "{files_txt_path}"')
    source_files = list_source_files(source, ignored_extensions)
    print(f'Found {len(source_files)} files in source.')
    if not os.path.exists(source):
        print(f'WARNING: Source directory "{source}" does not exist.')
    if not source_files:
        print('WARNING: No files found in source.')
    files_in_txt = read_files_txt(files_txt_path)

    # If files.txt does not exist, create it from source files
    if not os.path.exists(files_txt_path):
        write_files_txt(files_txt_path, source_files)
        print(f'Created files.txt at "{files_txt_path}" with {len(source_files)} files.')
        files_in_txt = source_files

    # Sync files: copy new/updated files from source to destination
    for rel_path in files_in_txt:
        src_path = os.path.join(source, rel_path)
        dst_path = os.path.join(destination, rel_path)
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(src_path):
            print(f'SKIP: "{rel_path}" not found in source.')
            continue
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
            shutil.copy2(src_path, dst_path)
            print(f'Copied: "{src_path}" -> "{dst_path}"')
        else:
            print(f'SKIP: "{rel_path}" already up-to-date.')

    # Remove files from destination not in files.txt if enabled
    if config.get("delete_extraneous_files", False):
        for root, _, filenames in os.walk(destination):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), destination)
                rel_path = rel_path.replace("\\", "/")
                if rel_path == FILES_TXT:
                    continue
                if rel_path not in files_in_txt:
                    os.remove(os.path.join(destination, rel_path))
                    print(f'Removed: "{os.path.join(destination, rel_path)}"')
    else:
        print("Keeping extraneous files on destination (delete_extraneous_files is False).")


def main():
    """Main entry point."""
    config = load_config()
    sync_files(config)
    print("Sync complete.")


if __name__ == "__main__":
    main()
