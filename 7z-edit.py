import os
import sys
import shutil
import tempfile
import subprocess
from getpass import getpass
import argparse

def szedit_print(*args, **kwargs):
    print("[7z-edit]", *args, **kwargs)
def szedit_input(prompt):
    return input("[7z-edit] " + prompt)
def szedit_getpass(prompt):
    return getpass("[7z-edit] " + prompt)
def szedit_exception(text, e = None):
    e_text = f"[7z-edit] Exception: {text}"
    if e: e_text += f" Details:\n{e}"
    return Exception(e_text)

def check_executable(executable):
    try:
        subprocess.run([executable, "-h"], capture_output=True, check=True)
    except Exception as e:
        raise Exception(f"{executable} is not installed or not in the PATH. Excecption: {e}")

def cleanup(temp_folder):
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
        szedit_print(f"Cleanup successful. Temporary folder {temp_folder} has been removed.")

def open_explorer(path):
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
        szedit_print(f"Failed to open the folder. Please open it manually at {path}.\nException: {e}")

def main():
    try:
        parser = argparse.ArgumentParser(description="Edit or create a compressed file.")
        parser.add_argument("-i", "--input", help="Path to the input file. If not specified, will create a  new file.", default=None)
        parser.add_argument("-o", "--output", help="Path to the output file. If not specified, the output filename will be the same as the input file with '_edited' appended.", default=None)

        args = parser.parse_args()
        input_file = args.input
        output_file = args.output
    
        if not input_file and not output_file:
            raise Exception(szedit_exception("At least one of the input file or the output file must be specified."))
    
        if input_file:
            if not os.path.exists(input_file):
                raise Exception(szedit_exception(f"The input file {input_file} does not exist."))
            if not output_file:
                output_file = f"{os.path.splitext(input_file)[0]}_edited{os.path.splitext(input_file)[1]}"

    except Exception as e:
        print(e)
        sys.exit(1)

    password = ""
    
    try:
        temp_folder = tempfile.mkdtemp()
        szedit_print(f"Working in temporary folder: {temp_folder}")
        
        check_executable("7z")
        
        if input_file:
            password = szedit_getpass("Enter the password for decryption and encryption (leave blank if none): ")
            try:
                subprocess.run(["7z", "x", f"-p{password}", input_file, f"-o{temp_folder}"], check=True)
            except Exception as e:
                raise szedit_exception("Decryption failed. Please check the password and try again.", e)
        
        szedit_print("Please edit the files in the temporary folder.")
        open_explorer(temp_folder)
        
        while True:
            szedit_print("Enter 'wq' to save and exit, 'q' to exit without saving, 'p' to reset the password")
            user_input = szedit_input(":").strip().lower()
            if user_input == 'wq':
                szedit_print(f"Compressing the updated files into {output_file}...")
                zip_command = ["7z", "a", output_file, f"{temp_folder}/*"]
                if password:
                    zip_command.insert(2, f"-p{password}")
                
                try:
                    subprocess.run(zip_command, check=True)
                except Exception as e:
                    raise szedit_exception("Zipping failed.", e)
                szedit_print(f"Process completed successfully. The updated file is {output_file}.")
                break
            elif user_input == 'q':
                szedit_print("Exiting without saving.")
                break
            elif user_input == 'p':
                password_new = szedit_getpass("Enter the new password (leave blank to remove the password): ")
                password_confirm = szedit_getpass("Enter the new password again: ")
                if password_new == password_confirm:
                    password = password_new
                    szedit_print("Password has been reset.")
                else:
                    szedit_print("Passwords do not match. Please try again.")
            else:
                szedit_print("Invalid input. Please try again.")
    
    except Exception as e:
        print(e)
        cleanup(temp_folder)
        sys.exit(1)
    
    cleanup(temp_folder)

if __name__ == "__main__":
    main()
