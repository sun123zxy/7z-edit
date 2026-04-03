# 7z-edit

## Description

Temporarily decrypt, checkout, edit, encrypt and rewrite a compressed file with ease.

## Installation

- 7-Zip installed and added to the system PATH
- Python if you wish to run the script directly

It's a standalone script / executable, so no installation is necessary.

### Register to Context Menu

On Windows, you can register or unregister 7z-edit to appear in the right-click context menu via executing the provided `.reg` file.

Add 7z-edit to your system PATH before doing so.

After registration, you can right-click any file and select "Edit with 7z-edit" to open it with the tool (with default parameters).

## Usage

```default
usage: 7z-edit [-h] [-i INPUT] [-o OUTPUT] [-l [LOG]] [filename]

Edit or create a compressed file.

positional arguments:
  filename             Alias for -i option.

options:
  -h, --help           show this help message and exit
  -i, --input INPUT    Path to the input file. If not specified, will create a new file.
  -o, --output OUTPUT  Path to the output file. If not specified, overwrite the original file.
  -l, --log [LOG]      Path to the log file. Disabled by default.
```

## Instructions

1. Run the script with the input file you want to edit.
2. Enter the password for decryption and encryption when prompted (leave blank if none).
3. The script will extract the contents to a temporary folder.
4. Edit the files in the temporary folder.
5. Enter `wq` to save and exit, `q` to exit without saving, `p` to reset the password, or `mv` rename.

## Notes

- Ensure that 7-Zip is installed and added to the system PATH.
- The temporary folder will be cleaned up automatically after the process is completed.
- Log files store the output of the 7-Zip command. Useful for debugging.

## License

This project is licensed under the MIT License.