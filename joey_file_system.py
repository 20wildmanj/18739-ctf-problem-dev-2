import random
import string
import os
import sys
import datetime
import traceback
import bcrypt
import magic
import sys
import tarfile
from pathlib import Path
import shutil
import subprocess

print(os.path.realpath(__file__))

USER_FILEPATH = Path("/home/ctf-player/downloads/").resolve()
FS_STORAGE_FILEPATH = Path("/home/joey_file_service/").resolve()
FLAG_PATH = Path("/home/joey_file_service/flag.txt").resolve()
MAX_LINES = 100

def upload_files(tar_filepath_name):
    os.chdir(USER_FILEPATH)
    tar_filepath = Path(tar_filepath_name).resolve()
    
    # Check if the file is within the directory
    if USER_FILEPATH not in tar_filepath.parents:
        print(f"ERROR: {tar_filepath_name} not in {USER_FILEPATH}")
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
    print("successfully uploaded", len(tar.get_members()), "files")
    return True
            
def cat_file(filepath_str):
    os.chdir(FS_STORAGE_FILEPATH)
    filepath = Path(filepath_str).resolve()
    
    # Check if the file is within the directory
    if FS_STORAGE_FILEPATH not in filepath.parents:
        print(f"ERROR: {filepath_str} not in {USER_FILEPATH}")
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
    return False
    
def get_file_info():
    # delete all user generated files
    for item in FS_STORAGE_FILEPATH.iterdir(): 
        if item.is_file() and item.name != "flag.txt":
            print(f"Deleting: {item}")
            item.unlink()


    


            
   

# ensure we aren't writing to an existing file
def _exists(fn):
    try:
        os.lstat(fn)
    except OSError:
        return False
    else:
        return True

# get ourselves a temporary file to write to
def temp_mktemp(prefix="", suffix=""):
    global rolling_counter
    dir = "/home/ctf-player/tmp/"

    names = _get_candidate_names()
    
    for i in range(TMP_MAX):
        i_circular = (rolling_counter + i) % TMP_MAX
        name = names[i_circular]
        file = os.path.join(dir, prefix + name + suffix)
        if not _exists(file):
            rolling_counter = rolling_counter + 1
            return file
        
    raise Exception("No usable temporary filename found")

# so our other admins can get the flag, they can slow down time so
# no issue if the file exists for only a moment
def write_flag_secure():
    temp_flag_file = temp_mktemp()
    flag = open("/challenge/flag.txt").read()
    now = datetime.datetime.now()
    append = " - DO NOT DISTRIBUTE - "
    append += f" - FROM: FLAG SERVER at time - {now}"
    # next level integrity hash!!!
    salt = bcrypt.gensalt()
    result = bcrypt.hashpw(
       password=append.encode('utf-8'),
       salt=salt
    )
    append += result.decode('utf-8')
    f = open(temp_flag_file, 'w+')
    f.write(flag)
    f.write(append)
    f.close()
    # admin has saved it with premonition, we can delete
    os.remove(temp_flag_file)
    print("wrote flag securely to: ", temp_flag_file)

def exit():
  sys.exit(0)

print("Welcome to the secure flag service! Only admins should use this service. Not like you could get the flag though, you operate too slowly to catch our flags.")

while(True):
  try:
    inp = input("put in command: ")
    if (inp == "temp"):
        write_flag_secure()
    elif(inp == "flag"):
       flag = open("/challenge/flag.txt").read()
       salt = bcrypt.gensalt()
       result = bcrypt.hashpw(
            password=flag.encode('utf-8'),
            salt=salt
       )
       print(flag)
       print("have fun with this!!!")
    elif (inp == "exit"):
       exit()
  except Exception as e:
    print("ERROR", e)
    print(traceback.format_exc())
    break