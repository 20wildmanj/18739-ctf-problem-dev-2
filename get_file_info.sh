#!/bin/bash
# script to do some cool stuff that definitely can't be done in python
FS_DIR="/home/joey_file_system/"
echo "files hosted on JFS: "
cd $FS_DIR && ls -lR | grep -v '^total' | grep -v 'flag.txt'
echo "doing MD5 integrity check..."
cd $REFERENCE_DIR && find . \( ! -regex '.*/\..*' \) -type f -exec md5sum \{\} \; | grep -v '/flag.txt' | sort -k2

echo "calculating cost"
RATE_PER_BYTE=0.0001  
COST_PER_FILE=0.05

# get num of files
FILE_COUNT=$(find "$FS_DIR" -type f | wc -l)
# ignore cost of flag file (they gotta pay for the bytes though)
FILE_COUNT=$((FILE_COUNT - 1))
TOTAL_SIZE=$(find "$FS_DIR" -type f -exec stat --format="%s" {} + | awk '{s+=$1} END {print s}')
 
if [ -z "$TOTAL_SIZE" ]; then
    TOTAL_SIZE=0
fi

COST_BY_SIZE=$(echo "$TOTAL_SIZE * $RATE_PER_BYTE" | bc)
COST_BY_FILE=$(echo "$FILE_COUNT * $COST_PER_FILE" | bc)
TOTAL_COST=$(echo "$COST_BY_SIZE + $COST_BY_FILE" | bc)

echo "Total number of files: $FILE_COUNT"
echo "Total size of files: $TOTAL_SIZE bytes"
echo "Cost by size: \$$(printf "%.5f" "$COST_BY_SIZE")"
echo "Cost by file count: \$$(printf "%.5f" "$COST_BY_FILE")"
echo "Total storage cost: \$$(printf "%.5f" "$TOTAL_COST")"
