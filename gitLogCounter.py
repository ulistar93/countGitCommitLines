import sys
import subprocess
import pdb

no_count_file_list = [None, 'MDSMLibVersion.cpp', 'MDSMLibrary.vcxproj', '.gitignore', '.gitmessage', 'MDSMLibrary.log']
no_count_file_keyword = ['LicenseInfo', 'PUX/', '.py', '.png', '.puml', '.TMP', 'include/', 'MDSMLibrary.vcxproj', 'Build.CppClean.log', 'lib.recipe', '.tlog']

def count_lines_list(git_show_output):
    if git_show_output is None:
        return 0, {}
    lines = git_show_output.split('\n')
    # pdb.set_trace()
    lines_per_file = {}
    current_file = None
    line_count = 0
    for line in lines:
        if current_file:
            if line.startswith('+') and not line.startswith('+++'):
                line_count += 1
            elif line.startswith('-') and not line.startswith('---'):
                line_count += 1
        if line.startswith('diff --git'):
            # file_a = line.split()[-2].split('/')[-1]
            # file_b = line.split()[-1].split('/')[-1]
            file_a = line.split()[-2][1:]
            file_b = line.split()[-1][1:]
            # if file_a != file_b:
            #     pdb.set_trace()
            current_file = file_b
            # if '/PUX/' in line:
            #     current_file='PUX/'+current_file
            line_count = 0
        if current_file is not None:
            lines_per_file[current_file] = line_count
    for file in list(lines_per_file.keys()):
        if lines_per_file[file] == 0:
            del lines_per_file[file]
    commit_total_lines = 0
    for file in list(lines_per_file.keys()):
        # if file not in no_count_file_list and (len([x in file for x in no_count_file_keyword])):
        if file not in no_count_file_list and "MDSM" in file and not any([x in file for x in no_count_file_keyword]):
            commit_total_lines += lines_per_file[file]

    return commit_total_lines, lines_per_file

def git_show_commit(commit_hash):
    # Run git show command for the given commit hash
    # command = ["git", "show", commit_hash]
    # command += ["|" "iconv -f euckr -t utf8"]
    command = ["/bin/bash", "git_show_utf8.sh", commit_hash]
    try:
        result = subprocess.run(command, capture_output = True, text=True, check=True, encoding="utf-8")
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding="utf-8")
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding="euckr")
        # return result.stdout.encode('euc-kr').decode('utf-8', 'ignore')
        # return result.stdout.decode('utf-8', 'ignore')
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing git show for commit {commit_hash}: {e}")
        # command += ["|" "iconv -f euckr -t utf8"]
        # result = subprocess.run(command, capture_output = True, text=True, encoding="utf-8")
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding="euckr")
        # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, encoding="utf-8")
        # return result.stdout.encode('euc-kr').decode('utf-8', 'ignore')
        pdb.set_trace()
        return None
    # return result.stdout

def parse_author(line):
    author_key = line.split()[0]
    if author_key == 'p':
        author = "park"
    elif author_key == 'o':
        author = line.split('<')[-1].split('>')[0]
    elif author_key == 'x':
        author = "x"
    return author

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python gitLogCounter.py <git_log_file>")
        # not allow ANSI colors in git_log_file
        sys.exit(1)
    git_log_file = sys.argv[1]
    commit_list = []
    for line in open(git_log_file, 'r'):
        if '*' not in line:
            continue
        line = line.strip() # "o * | 2bdb760 - (tag: v2.0) Merge.. <Changmin Yi>"
        lineC = '*'.join(line.split('*')[1:]).strip() # "| 2bdb760 - (tag: v2.0) Merge.. <Changmin Yi>"
        lineC = lineC.split('-')[0].strip() # "| 2bdb760"
        hash = lineC.split()[-1] # "2bdb760"
        if len(hash) != 7:
            pdb.set_trace()
        # author = line.split()[0]
        author = parse_author(line)
        if author != 'x':
            git_show_output = git_show_commit(hash)
        else:
            git_show_output = None
        num_lines, num_lines_detail = count_lines_list(git_show_output)
        # num_lines = count_lines(git_show_output)
        print([author, hash, num_lines, num_lines_detail])
        commit_list.append([author, hash, num_lines, num_lines_detail])
        # pdb.set_trace()
    with open('20240425_all.txt', 'w') as f:
        for commit in commit_list:
            f.write(str(commit)+'\n')
    commit_summary = {}
    for commit in commit_list:
        if commit[0] not in commit_summary:
            commit_summary[commit[0]] = 0
        commit_summary[commit[0]] += commit[2]
    with open('20240425_summary.txt', 'w') as f:
        f.write(str(commit_summary))
    pdb.set_trace()