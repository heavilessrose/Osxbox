import os
import subprocess

print os.getpid()
p = subprocess.Popen(("samples/test"))

print p.pid

