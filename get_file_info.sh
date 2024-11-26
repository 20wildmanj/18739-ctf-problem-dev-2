FS_DIR="/home/joey_file_service/"
cd $FS_DIR && ls -lR | grep -v '^total' | grep -v 'flag.txt'
