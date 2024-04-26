#!/bin/bash

source ~/torch1.8/bin/activate

# git show $1 | iconv -f euckr -t utf8
# git show $1 | iconv -f CP949 -t utf8
# git show $1 | iconv -f utf8 -t utf8
git show $1 > gitshow.tmp
# file -bi gitshow.tmp

# 문제가 되는 commit
# utf-8 kr 09ae5ab
# euckr 9a6849e
# mixed 0edd9e0

# 파일 단위 변환
file_info=$(file -bi gitshow.tmp)
file_charset=$(echo "$file_info" | sed -n 's/.*charset=\([^;]*\).*/\1/p')
if [ "$file_charset" == "utf-8" ]
then
    usleep 1
elif [ "$file_charset" == "iso-8859-1" ]
then
    cat gitshow.tmp | iconv -f euckr -t utf8 > gitshow.tmp.utf8
else
    # 라인 단위 변환
    echo "" > gitshow.tmp.utf8
    while IFS= read -r line; do
        # line_charset=$(echo "$line" | file -bi -)
        line_charset=$(echo "$line" | file -bi - | sed -n 's/.*charset=\([^;]*\).*/\1/p')
        if [ "$line_charset" == "iso-8859-1" ]; then
            echo "$line" | iconv -f euckr -t utf8 >> gitshow.tmp.utf8
        elif [ "$line_charset" == "unknown-8bit" ]; then
            # echo "$line" | iconv -f euckr -t utf8 > gitshow.tmp.utf8 # fail
            echo "$line" | iconv -f CP949 -t utf8 >> gitshow.tmp.utf8
        else
            echo "$line" >> gitshow.tmp.utf8
        fi
    done < gitshow.tmp
fi

mv gitshow.tmp.utf8 gitshow.tmp
cat gitshow.tmp