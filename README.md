# Car USB File Synchronizer

A simple Python tool to synchronize music files between your local drive and your car's USB drive. Uses a `files.txt` on the USB as the source of truth for what should be present.

## Features

- Syncs files from a local source directory to a USB destination.
- Uses `files.txt` at the USB root as the authoritative list of files.
- Ignores files with specified extensions.
- Optionally deletes files on the USB not listed in `files.txt`.
- Clear logging for all actions (copy, skip, remove, warnings).

## Requirements

- Python 3.6 or higher
- Windows OS (paths use Windows format)

## Installation

1. Clone this repository or download the files.
2. Place `sync.py` and `config.json` in the same directory.

## Configuration

Edit `config.json` to set your paths and options:

```json
{
  "source": "C:/Music",
  "destination": "E:/",
  "ignored_extensions": [".tmp", ".log", ".ini"],
  "delete_extraneous_files": false
}
```

- `source`: Path to your local music folder.
- `destination`: Path to your USB drive (e.g., `E:/`).
- `ignored_extensions`: List of file extensions to ignore.
- `delete_extraneous_files`: If `true`, files on the USB not in `files.txt` will be deleted. If `false` (default), they will be kept.

## Usage

1. Make sure your USB is plugged in and the paths in `config.json` are correct.
2. Run the synchronizer:

```sh
python sync.py
```

3. The script will:
   - Create `files.txt` on the USB if it does not exist (listing all source files).
   - Copy new or updated files from the source to the USB.
   - Optionally remove files from the USB not in `files.txt` (if enabled).
   - Log all actions to the terminal.

## How It Works

- `files.txt` at the USB root lists all files that should be present.
- On first run, if `files.txt` does not exist, it is created from the source.
- On subsequent runs, only files listed in `files.txt` are synced.
- Files not in the source are skipped, and you are notified.
- If `delete_extraneous_files` is `true`, files not in `files.txt` are deleted from the USB.

## Example Output

```
Source: "C:/Music"
Destination: "E:/"
files.txt path: "E:/files.txt"
Found 123 files in source.
Created files.txt at "E:/files.txt" with 123 files.
Copied: "C:/Music/song1.mp3" -> "E:/song1.mp3"
SKIP: "song2.mp3" already up-to-date.
Removed: "E:/old_song.mp3"
Sync complete.
```

## License

MIT License
