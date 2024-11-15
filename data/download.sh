#!/bin/sh

DST=""
PORT=""
USERNAME=""
PASSWORD=""

NUM_FILES=2000

# 1. FTP 서버에 접속하여 파일 목록을 최신 순으로 가져오기
ftp -p -n <<END_SCRIPT | awk '{print $NF}' | grep -v "3d" | tail -n $NUM_FILES > file_list.txt
open $DST $PORT
user $USERNAME $PASSWORD
cd /pore
ls -t
bye
END_SCRIPT

# 2. file_list.txt에서 최신 파일 이름을 뽑아내고 wget으로 다운로드
for file in $(cat file_list.txt); do
    wget -q --user=$USERNAME --password=$PASSWORD ftp://$DST:$PORT/pore/$file -O ./pore/$file -o /dev/null
done
