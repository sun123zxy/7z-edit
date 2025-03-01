import os
import shutil
import tempfile
import subprocess
from getpass import getpass
import argparse

def check_executable(executable):
    result = subprocess.run(["where", executable], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error: {executable} is not installed or not in the PATH.")

def cleanup(temp_folder):
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
        print(f"Cleanup successful. Temporary folder {temp_folder} has been removed.")

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
        print(f"Error: Failed to open the folder. Please open it manually at {path}. Exception: {e}")

def main():
    parser = argparse.ArgumentParser(description="Edit a compressed file.")
    parser.add_argument("zip_file", help="The zip file to edit.")
    parser.add_argument("-o", "--output", help="The name of the output file. If not specified, the output filename will be the same as the input file with '_edited' appended.", default=None)

    args = parser.parse_args()
    zip_file = args.zip_file
    
    if not os.path.exists(zip_file):
        print(f"Error: The file {zip_file} does not exist.")
        return
    
    password = getpass("Enter the password for decryption and encryption (leave blank if none): ")
    
    new_zip_file = args.output if args.output else f"{os.path.splitext(zip_file)[0]}_edited{os.path.splitext(zip_file)[1]}"
    
    try:
        temp_folder = tempfile.mkdtemp()
        print(f"Working in temporary folder: {temp_folder}")
        
        check_executable("7z")
        
        unzip_result = subprocess.run(["7z", "x", f"-p{password}", zip_file, f"-o{temp_folder}"])
        if unzip_result.returncode != 0:
            raise Exception("Error: Extraction failed. Please check the password and try again.")
        
        print("Please edit the files in the temporary folder.")
        open_explorer(temp_folder)
        
        # Wait for the user to finish editing the files
        # Meanwhile, the user have the following options:
        # 1. Enter wq to save and exit
        # 2. Enter q to exit without saving
        # 3. Enter p to reset the password 
        while True:
            print("Enter 'wq' to save and exit, 'q' to exit without saving, 'p' to reset the password")
            user_input = input(":").strip().lower()
            if user_input == 'wq':
                print(f"Compressing the updated files into {new_zip_file}...")
                zip_command = ["7z", "a", new_zip_file, f"{temp_folder}/*"]
                if password:
                    zip_command.insert(2, f"-p{password}")
                zip_result = subprocess.run(zip_command)
                if zip_result.returncode != 0:
                    raise Exception("Error: Zipping failed.")
                print(f"Process completed successfully. The updated file is {new_zip_file}.")
                break
            elif user_input == 'q':
                print("Exiting without saving.")
                break
            elif user_input == 'p':
                password_new = getpass("Enter the new password (leave blank to remove the password): ")
                # enter the new password again to confirm
                password_confirm = getpass("Enter the new password again: ")
                if password_new == password_confirm:
                    password = password_new
                    print("Password has been reset.")
                else:
                    print("Passwords do not match. Please try again.")
            else:
                print("Invalid input. Please try again.")
    
    except Exception as e:
        print(e)    
    
    finally:
        cleanup(temp_folder)

if __name__ == "__main__":
    main()
