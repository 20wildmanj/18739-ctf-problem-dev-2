#!/bin/bash

set -e

service ssh start

socat tcp-listen:5556,reuseaddr,fork SYSTEM:"python3 /home/joey_file_system_exec/joey_file_system.py" &
socat tcp-listen:5555,reuseaddr,fork tcp:localhost:22
