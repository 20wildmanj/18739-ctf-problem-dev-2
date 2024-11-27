# Joey File System

- Namespace: picoctf/18739f24
- ID: jwildman-problem-dev-2
- Type: custom
- Category: System fundamentals
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

I made an amazing new file system called joey file system (JFS)! It allows you to upload
your files to my file system, which get securely stored in the joey cloud. You can
download your files, view your files, and check their costs all through this CLI. I may
have left in some confidential information in the file system but I think I made sure
you can't access it. At least I think?

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

Then run `$ nc 5556` inside the ssh

## Hints

- I tried my best to make sure all files stay within the file system, but I'm not quite
  sure that they do.

## Solution Overview

My solution involves using a tarslip vulnerability to rewrite the shell script used
to calculate the "cost" of the files currently stored in the file system. If you
upload a tar file with a relative path (e.g. `../joey_file_system_exec/--`) then you can
then upload files into that folder, when it is inaccessible otherwise (can't view / overwrite).
Uploading such a malicious tarfile using the `upload_files` endpoint, and then running
a malicious script to cat the flag using the `get_file_info` command will then net you
the flag.

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
diskquota: 64m
init: true
```

## Learning Objective

A showcase of path traversal vulnerabilities and how relative paths can be abused to gain
access to parts of a file system that were not intended to be accessible. Also using
shell scripting to get the flag.

## Tags

- ssh
- bash
- linux

## Attributes

- author: Joey Wildman (jwildman)
- organization: 18739
- event: 18739 Problem Development 2
