# countGitCommitLines


### git lg (oneline log)
```
git config --global alias.lg "log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all"
```

### how to use
- save the git lg into file `gitlg.sh`
- add author mark 'o' or 'p' or else what you want (ex) `gitlg2.txt` fix -> `gitlg3.txt`
- run py `python3 gitLogCounter.py`
    - `gitLogCounter.py` use `git_show_utf8.sh` internally with subprocess

### TroubleShooting
- 특정 commit에서 파일인코딩에 의해 끊길 수 있음
- utf-8, 한글(CP949, iso-8859-1, euckr)등이 섞여있을 경우 unknown-8bit로 표기됨
- `git_show_line_format_test.sh`를 통해서 각 줄마다 (line-by-line) 포맷을 확인
    - `git_show_line_format_test.sh`는 `git_show_line_format_test.py`를 사용함