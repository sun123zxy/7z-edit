import os
import sys
import shutil
import tempfile
import subprocess
from getpass import getpass
import argparse

class SZEditException(Exception):
    def __init__(self, message, details = None):
        self.message = message
        self.details = details
    def __str__(self):
        # add indentation before all lines of details
        text = "[7z-edit] [Exception] "
        text += str(self.message)
        if self.details:
            text += " Details:\n"
            text += "".join(["  " + line + "\n" for line in str(self.details).split("\n")])
            text = text[:-1] if text[-1] == "\n" else text # remove the last newline character if exists
        return text

def szedit_print(*args, **kwargs):
    print("[7z-edit]", *args, **kwargs)
def szedit_input(prompt):
    return input("[7z-edit] " + prompt)
def szedit_getpass(prompt):
    return getpass("[7z-edit] " + prompt)

def check_executable(executable):
    try:
        subprocess.run([executable, "-h"], capture_output=True, check=True)
    except Exception as e:
        raise SZEditException(f"{executable} is not installed or not in the PATH.", e)

def cleanup(*args):
    for temp_folder in args:
        if temp_folder and os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
            szedit_print(f"Successfully cleaned up the temporary folder {temp_folder}.")

def try_open_explorer(path):
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["explorer", path])
        elif os.name == 'posix':  # macOS or Linux
            if sys.platform == 'darwin':  # macOS
                subprocess.run(["open", path])
            else:  # Linux
                subprocess.run(["xdg-open", path])
        else:
            raise Exception("Unsupported OS.")
    except Exception as e:
        print(SZEditException(f"Failed to open the temporary folder. Please open it manually.", e))

def main():

    # --- Setup argument parser ---=
    parser = argparse.ArgumentParser(
        prog="7z-edit",
        description="Edit or create a compressed file.",
        exit_on_error=False)
    parser.add_argument("filename", help="Path to the file to edit. Non-existent file will be created.")
    parser.add_argument("-l", "--log", nargs="?", const="7z-edit.log", help="Path to the log file. Disabled by default.")
    
    # --- Parse arguments ---
    try:
        args = parser.parse_args()
        input_file = args.filename
        output_file = args.filename
        log_file = args.log
    except Exception as e:
        print(SZEditException("Error parsing arguments.", e))
        sys.exit(1)
    
    try:
        # --- Check if 7z is installed ---
        check_executable("7z")
    except Exception as e:
        print(e)
        sys.exit(1)

    # --- Main process ---
    try:
        # --- Create a temporary folder ---
        temp_input_folder = tempfile.mkdtemp()
        temp_output_folder = tempfile.mkdtemp()
        
        # --- handle log file ---
        f = open(log_file, "a") if log_file else open(os.path.join(temp_output_folder, "7z-edit.log"), "a") # output to nowhere if log_file is None

        # --- Decompress the input file ---
        password = ""
        if os.path.exists(input_file):
            password = szedit_getpass("Enter the password for decryption and encryption (leave blank if none): ")
            try:
                unzip_command = ["7z", "x", "-y", f"-p{password}", input_file, f"-o{temp_input_folder}"]
                subprocess.run(unzip_command, check=True, stdout=f, stderr=f)
            except Exception as e:
                raise SZEditException("Decompression failed. Check your password or the file integrity.", e)
            szedit_print("Decompression complete.")
        else:    
            szedit_print("Input file does not exist. Initialize with an empty folder.")
    
        # --- Try open the folder in file explorer ---
        szedit_print(f"Please edit the files in the temporary folder {temp_input_folder}...")
        try_open_explorer(temp_input_folder)
    
        # --- Wait for user to finish editing ---
        while True:
            szedit_print("Enter 'wq' to save and exit, 'q' to exit without saving, 'p' to reset the password, 'mv' to rename")
            user_input = szedit_input(":").strip().lower()

            # --- Save and exit ---
            if user_input == 'wq': 
                # --- Zip the files ---
                temp_output_file = os.path.join(temp_output_folder, os.path.basename(output_file))
                szedit_print(f"Compressing the updated files into a temporary file {temp_output_file}...")
                try:
                    zip_command = ["7z", "a", temp_output_file, f"{temp_input_folder}/*"]
                    if password: zip_command.insert(2, f"-p{password}")
                    subprocess.run(zip_command, check=True, stdout=f, stderr=f)
                except Exception as e:
                    raise SZEditException("Compression failed.", e)
                
                # --- Move the output file to the correct location ---
                szedit_print(f"Moving {temp_output_file} to {output_file}...")
                try:
                    shutil.move(temp_output_file, output_file)
                except Exception as e:
                    raise SZEditException("Failed to move the output file.", e)
                
                szedit_print(f"Process complete. The updated file is {output_file}.")
                
                # --- Delete the input file if it's different from the output file ---
                if input_file != output_file:
                    try:
                        os.remove(input_file)
                        szedit_print(f"Deleted the original input file {input_file}.")
                    except Exception as e:
                        szedit_print(f"Warning: Failed to delete the input file {input_file}. {str(e)}")
                
                break

            # --- Exit without saving ---
            elif user_input == 'q':
                szedit_print("Exiting without saving.")
                break

            # --- Reset password ---
            elif user_input == 'p':
                password_new = szedit_getpass("Enter the new password (leave blank to remove the password): ")
                password_confirm = szedit_getpass("Enter the new password again: ")
                if password_new == password_confirm:
                    password = password_new
                    szedit_print("The password has been reset.")
                else:
                    szedit_print("New passwords do not match. The password has not been reset. Please try again.")

            # --- Change the output file name ---
            elif user_input == 'mv':
                new_output_file = szedit_input(f"Enter the new output file path (current: {output_file}): ").strip()
                if new_output_file:
                    output_file = new_output_file
                    szedit_print(f"The output file has been changed to {output_file}.")
                else:
                    szedit_print("Output file unchanged.")

            # --- Invalid input ---
            else:
                szedit_print("Invalid input. Please try again.")
    
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if f: f.close()
        cleanup(temp_input_folder, temp_output_folder)
        if log_file: szedit_print(f"Log saved at {log_file}")

if __name__ == "__main__":
    main()
