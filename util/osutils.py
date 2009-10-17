import os
import shutil

def touch(path):
    makedirs_p(os.path.dirname(path))
    f = open(path, 'w')
    f.close()

def makedirs_p(path):
    if not os.access(path, os.F_OK):
        os.makedirs(path)

def rmdir_p(path):
    shutil.rmtree(path)

def write_to_file(path, content):
    makedirs_p(os.path.dirname(path))
    f = open(path, 'w')
    try:
        f.write(content)
    finally:
        f.close()

os.write_to_file = write_to_file
os.touch = touch
os.makedirs_p = makedirs_p
os.rmdir_p = rmdir_p


