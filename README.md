# Problem Dev 1

This problem's infrastructure is based on the "general-ssh" example found in the
[picoCTF/start-problem-dev](https://github.com/picoCTF/start-problem-dev/tree/master/example-problems/general-ssh)
github page.

Run this example with cmgr to be able to playtest it. Find instructions on the actual problem at `problem.md`

```
cmgr update
cmgr playtest 18739/jwildman-problem-dev-1
```

If you are playtesting, you can run the generic solver:
`python3 solution_general.py SSH_PORT PASSWORD`

## Overall Idea

The idea for this problem came from learning about a published vulnerability
in the `mktemp` function which for example exists as a python function in
the tempfile library. I was made aware of a mktemp vulnerability in a 
repository I help to maintain, so by researching what that vulnerability
entailed, I came up with this problem. There are published CVEs from
for example [Tensorflow](https://nvd.nist.gov/vuln/detail/CVE-2022-23563),
and more information on the function's weaknesses can be found at
tempfile's [documentation website](https://docs.python.org/3/library/tempfile.html).

I created a vastly simplified version of mktemp that would allow for someone to
somewhat easily figure out how to predict what the temporary file name would
be so that they could then create for example a symlink pointing that file name
to an attacker-controlled file before the file got created and written to,
so that they could then read the file and get the flag. I also added in some
intermediary computation between invoking mktemp and opening the file so
that there would be a good chunk of time in order to then create the symlink
between the mktemp invocation and the file open, to facilitate an easy
TOCTOU attack.

One issue I ran into during the development of this problem was that if the 
temporary files are stored in /tmp, due to some linux kernel settings that
prevent opens of files not owned by the user in world-writable sticky directories
(see [this link](https://unix.stackexchange.com/questions/691441/root-cannot-write-to-file-that-is-owned-by-regular-user)).

To bypass this, I ended up putting the temporary files in a separate directory,
meaning that this problem might have lost some realisticness, but this was
necessary in order for this kind of TOCTOU to actually work.

The version of mktemp I implemented has a pool of random file names that are
generated at runtime, between 10 and 20. When mktemp is invoked, it will
go through the pool of names, and select them one by one. If it finds that
a file with the selected name already exists, it will then try to use
the next name in the pool, and so on, which means that the only real exploit
is through a TOCTOU attack. However, because the pool is finite in size, and
is re-used linearly, the sequence of random names used can be predicted
allowing for us to figure out the next temporary file name before invoking
the temp command.

The temp_file_madness script is run as a service on port 5556 and can be
connected to using netcat. The intended flow is for a user to ssh to the
host container and then netcat to the service. They can use the container
to figure out where the temporary files go / run the symlink commands
necessary to do the exploit.