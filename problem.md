# General SSH

- Namespace: 18739
- ID: jwildman-problem-dev-2
- Type: custom
- Category: System fundamentals
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

Do you know how to move between directories and read files in the shell?

## Details

`ssh -p {{port("ssh")}} ctf-player@{{server("ssh")}}` using password
`{{lookup("password")}}`

Then run `$ nc {{server}} {{port}}` / `nc localhost {{port}}` inside the ssh

## Hints

- There's a reason mktemp is deprecated, why are they making their own implementation of it?

## Solution Overview

figure out the temp file locations by submitting "temp" command a bunch of times.
Then once you know the temp file location, you can then create a symlink in between the time
the temp file location is generated and when its opened so you can then get the flag (TOCTOU).

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

Showcasing how TOCTOU can actually be possible in the real world by mimicking an actual vulnerability
in a modified version of mktemp

## Tags

- ssh
- bash
- example

## Attributes

- author: Joey Wildman (jwildman)
- organization: 18739
- event: 18739 Problem Development 1
