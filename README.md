# 7z-edit

## Description

A simple command line tool to ease the cumbersome process of editing a (possibly encrypted) compressed file. Should work on any compressed file format supported by 7-Zip.

## Requirements

- 7-Zip installed and added to the system PATH
- (Optional) Python 3.x if you wish to run the script directly

Developed on Windows 11 with Python 3.13.2 and 7-Zip 22.00. Windows executables are provided in releases. Should work on other platforms as well, but this is not well-tested.

## Usage

```default
usage: 7z-edit [-h] [-i INPUT] [-o OUTPUT]

Edit or create a compressed file.

options:
  -h, --help           show this help message and exit
  -i, --input INPUT    Path to the input file. If not specified, will start from scratch.
  -o, --output OUTPUT  Path to the output file. If not specified, the output filename will be the same as the input file with '_edited' appended.
```

## Instructions

1. Run the script with the input file you want to edit.
2. Enter the password for decryption and encryption when prompted (leave blank if none).
3. The script will extract the contents to a temporary folder.
4. Edit the files in the temporary folder.
5. Enter `wq` to save and exit, `q` to exit without saving, or `p` to reset the password.
6. If `wq` is entered, the script will compress (and encrypt) the updated files into the specified output file.

## Notes

- Ensure that 7-Zip is installed and added to the system PATH.
- The temporary folder will be cleaned up automatically after the process is completed.
- Both the script and this README are written in collaboration with Github Copilot. Be aware of potential errors or inaccuracies.

## License

This project is licensed under the MIT License.