import subprocess, pdb

command = ["cat", "gitshow.tmp.utf8"]
print(command)
# result = subprocess.run(command, capture_output = True, text=True, check=True, encoding="utf-8")
try:
    result = subprocess.run(command, capture_output = True, text=True, encoding="utf-8")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"**Error**: {e}")
# pdb.set_trace()