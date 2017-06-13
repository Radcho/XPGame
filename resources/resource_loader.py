import os
dir = os.path.dirname(__file__)

files = {}

for (dirpath, dirnames, filenames) in os.walk(dir):
    for file in filenames:
        files[file] = dirpath + "\\" + file
