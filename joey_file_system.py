import os
import sys
import datetime
import traceback
import magic
import sys
import tarfile
from pathlib import Path
import shutil
import subprocess

print(os.path.realpath(__file__))

USER_FILEPATH = Path("/home/ctf-player/downloads/").resolve()
FS_STORAGE_FILEPATH = Path("/home/joey_file_system/").resolve()
FS_EXEC_FILEPATH = Path("/home/joey_file_system_exec/get_file_info.sh").resolve()
FLAG_PATH = Path("/home/joey_file_system/flag.txt").resolve()
MAX_LINES = 100

def upload_files(tar_filepath_name):
    os.chdir(USER_FILEPATH)
    tar_filepath = Path(tar_filepath_name).resolve()
    
    # Check if the file is within the directory
    if USER_FILEPATH not in tar_filepath.parents:
        print(f"ERROR: {tar_filepath_name} not in {USER_FILEPATH}")
        return False
    
    if not tar_filepath.exists() or not tar_filepath.is_file():
        print(f"ERROR: {tar_filepath_name} is not a file!")
        return False

    print("FILE:", magic.from_file(tar_filepath_name))
    with tarfile.open(tar_filepath_name) as tar:
        for entry in tar:
            # do security checks
            if "flag.txt" in entry.name:
                continue
            if os.path.isabs(entry.name):
                print(f"Ignored illegal tar archive entry {entry.name}")
            
            tar.extract(entry, FS_STORAGE_FILEPATH)
        print("successfully uploaded", len(tar.getnames()), "files")
    return True
            
def cat_file(filepath_str):
    os.chdir(FS_STORAGE_FILEPATH)
    filepath = Path(filepath_str).resolve()
    
    # Check if the file is within the directory
    if FS_STORAGE_FILEPATH not in filepath.parents:
        print(f"ERROR: {filepath_str} not in {FS_STORAGE_FILEPATH}")
        return False
    elif FLAG_PATH == filepath:
        print(f"ERROR: cannot cat this file")
        return False
    
    count = 0
    if (filepath.exists()):
        with filepath.open("r") as file:
            for line in file:
                print(line.strip())
                if (count > MAX_LINES):
                    break
                count += 1
    
    if (count > MAX_LINES):
        print(f"(output truncated to {MAX_LINES} lines)")

def download_file(filepath_str):
    os.chdir(FS_STORAGE_FILEPATH)
    filepath = Path(filepath_str).resolve()
    # Check if the file is within the directory
    if FS_STORAGE_FILEPATH not in filepath.parents:
        print(f"ERROR: {filepath_str} not in {USER_FILEPATH}")
        return False
    elif FLAG_PATH == filepath:
        print(f"ERROR: cannot download this file")
        return False
    elif not filepath.is_file() or not filepath.exists():
        print(f"ERROR: file doesn't exist?")
        return False
    
    shutil.copy(filepath, USER_FILEPATH)
    print(f"downloaded {filepath_str} to {USER_FILEPATH}")

def reset_file_system():
    if not FS_STORAGE_FILEPATH.exists() or not FS_STORAGE_FILEPATH.is_dir():
        print("FATAL: FS STORAGE DOESN'T EXIST?")
        return False
    # delete all user generated files
    for item in FS_STORAGE_FILEPATH.iterdir(): 
        if item.is_file() and item.name != "flag.txt":
            print(f"Deleting: {item}")
            item.unlink()
    return True
    
def get_file_info():
    # get info of the files using custom script
    result = subprocess.run(["bash", FS_EXEC_FILEPATH], capture_output=True, text=True)

    # Print the output and errors
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    print("Return Code:", result.returncode)

def exit():
  sys.exit(0)

print("Joey File System (JFS) version 1.0.0.")
print("MESSAGE: We guarantee your files are super safe and secure using our proprietary storage algorithms!")

while(True):
  try:
    inp = input("USER COMMAND: ")
    user_args = inp.split()

    if not user_args:
        print(f"ERROR: Unknown command. Type 'help' for a list of commands.")
        continue

    if (user_args[0] == "help"):
        print("OPTIONS: ")
        print("-"*20)
        print("upload_files - upload files to JFS. Must be tar, and tar must be in downloads folder.")
        print("cat_file: preview your file stored in JFS")
        print("download_file: download file stored in JFS back to user downloads.")
        print("reset_file_system: reset the file system (delete everything)")
        print("get_file_info: get info about all stored files, and current cost of running JFS")
        print("exit: exit JFS")
        print("-"*20)
    elif user_args[0] == "upload_files":
        if len(user_args) < 2:
            print("ERROR: 'upload_files' requires a filename argument.")
        else:
            if (upload_files(user_args[1])):
                print("Successfully uploaded files!")
    elif user_args[0] == "cat_file":
        if len(user_args) < 2:
            print("ERROR: 'cat_file' requires a filename argument.")
        else:
            cat_file(user_args[1])
    elif user_args[0] == "download_file":
        if len(user_args) < 2:
            print("ERROR: 'download_file' requires a filename argument.")
        else:
            if (download_file(user_args[1])):
                print("succesfully downloaded file")
    elif user_args[0] == "reset_file_system":
        res = reset_file_system()
        if res:
            print("Successfully reset JFS.")
    elif user_args[0] == "get_file_info":
        get_file_info()
    elif user_args[0] == "exit":
        exit()
    else:
        print(f"ERROR: Unknown command '{user_args[0]}'. Type 'help' for a list of commands.")

  except Exception as e:
    print("ERROR", e)
    print(traceback.format_exc())
    break
  

