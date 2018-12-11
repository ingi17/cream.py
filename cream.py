import sys
from os import walk

folder = sys.argv[1]
#target = sys.argv[2]

filenames = []
folders = []
path = []

for (dirpath, dirnames, fnames) in walk(folder):
    filenames.extend(fnames)
    folders.extend(dirnames)
    path.append(dirpath)

print(path)