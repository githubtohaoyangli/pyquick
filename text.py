import re
r1=r'amd64a\d+/'
r3=r'win32a\d+/'
r2=r'arm64a\d+/'
r4=r'amd64/'
r5=r'win32/'
r6=r'arm64/'
print(re.match(r4, 'python3.140a4-amd64.exe'))