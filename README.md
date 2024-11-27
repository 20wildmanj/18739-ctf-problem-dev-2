# Problem Dev 1

This problem's infrastructure is based on the "general-ssh" example found in the
[picoCTF/start-problem-dev](https://github.com/picoCTF/start-problem-dev/tree/master/example-problems/general-ssh)
github page. It also builds on my problem-dev-1 work in that the overall
structure was built off that repo.

Run this example with cmgr to be able to playtest it. Find instructions on the actual problem at `problem.md`

```
cmgr update
cmgr playtest 18739/jwildman-problem-dev-1
```

If you are playtesting, you can run the generic solver `solve.py`. 
I couldn't get the cmgr solver to work as for some reason it couldn't
pip install from requirements.txt. But the top-level solve file works
if you run it against the playtest. As part of the solver I included a malicious
tar file that is necessary for the solution to work.
`python3 solve.py SSH_PORT PASSWORD`

## Overall Idea

Similar to the previous assignment, I derived my inspiration for this
problem from real-world CVEs. In particular, I had known about
[tarslip vulnerabilities](https://codeql.github.com/codeql-query-help/python/py-tarslip/)
for some time and this vulnerability still shows up from [time to time](https://nvd.nist.gov/vuln/detail/CVE-2024-2914). I also have been taking the Storage Systems class in which I have
been implementing a file system so I thought it would be cool to combine the concept of
a dummy file system with some sort of vulnerability. Based on those two initial points
of inspiration I came up with the concept for this CTF problem.

I essentially mocked up a super lightweightversion of a file system where you could upload files to it,
read the file, download the files, and remove the files, although it's really more of an
append-only file system with how to remove file you need to reset the entire file system. This file
system keeps all of the stored files uploaded by the user in a protected folder that the user can't
access normally, in `/home/joey_file_service/`. The flag is also stored in joey_file_service, but trying
to view the file through JFS results in an error. 

The actual script that runs joey_file_service and
another script that helps facilitate getting file information then live in `/home/joey_file_service_exec/`,
which is also protected from the user. This script is simply a bash script that does some random stuff like
list out all the files currently stored in the folder, calulcate their MD5 sums, and then come up with a total
"cost" of storing all those files. This script is called by the JFS python script when the `get_file_info` command
is invoked by the user.

Therefore, the main attack vector that I have created with this setup is through the `upload_files` command.
It takes in a tarfile and untars it inside the `joey_file_service_exec` folder. This command has some
checks for tar file entries, such as preventing overwriting of the flag and barring absolute pathnames, but
it does not bar relative paths such as `../`. Therefore, it is possible to provide a tarfile entry
that expands out to `../joey_file_service_exec/get_file_info.sh` which would then overwrite the shell script
for `get_file_info`. Then, on a subsequent call of `get_file_info`, the
overwritten script file gets called, which could for example contain a cat command to print out the flag.txt
file. I assume you could also spawn a shell / RCE but that is not necessary to solve this problem.

The other methods I implemented (`download_file`, `view_file`) serve as more of a distraction where they
do also involve file paths but they have more explicit checks to ensure the file paths that are used
lie within the actual file path of the user so they can't really do anything nefarious with them.

In order to mitigate the vulnerability demonstrated in this CTF problem, when extracting out a tar file,
you should always explicitly check to ensure the destination of the extracted file lies within the working 
directory, and ignore relative paths / expand them to fully absolute paths to do the check. There are
also ways to do this automatically using the `tarfile` library using filters when extracting so you
don't have to worry about doing this manually.
