#!/bin/bash

git lg > gitlg.txt
sed gitlg.txt -e 's/\x1b\[[0-9;]*m//g'> gitlg2.txt
