# 7z-edit

## Description

A simple command line tool to ease the cumbersome process of editing the contents of a (possibly encrypted) compressed file. Theoretically, any compressed file format supported by 7-Zip is supported.

## Requirements

- 7-Zip installed and added to the system PATH
- (Optional) Python 3.x if you wish to run the script directly

Developed on Windows 11 with Python 3.13.2 and 7-Zip 22.00. Windows executables are provided in releases. Should work on other platforms as well, but this is not tested.

## Usage

```sh
7z-edit <zip_file> [-o <output_file>]
```

- `zip_file`: The path to the zip file you want to edit.
- `-o, --output`: (Optional) The name of the output file. If not specified, the output filename will be the same as the input file with `_edited` appended.

## Instructions

1. Run the script with the zip file you want to edit.
2. Enter the password for decryption and encryption when prompted (leave blank if none).
3. The script will extract the contents to a temporary folder.
4. Edit the files in the temporary folder.
5. Enter `wq` to save and exit, `q` to exit without saving, or `p` to reset the password.
6. If `wq` is entered, the script will compress the updated files into the specified output file.

## Notes

- Ensure that 7-Zip is installed and added to the system PATH.
- The temporary folder will be cleaned up automatically after the process is completed.
- Both the script and this README are written in collaboration with Github Copilot. Be aware of potential errors or inaccuracies.

## License

This project is licensed under the MIT License.