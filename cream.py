import sys
import re
from os import walk

folder = sys.argv[1]
#target = sys.argv[2]

filenames = []
folders = []
path = []

def setlists(folder):
    for (dirpath, dirnames, fnames) in walk(folder):
        filenames.extend(fnames)
        folders.extend(dirnames)
        path.append(dirpath)

setlists(folder)

def getSeries(fnames):
    regex = re.compile('((s|S)\d+)|(\d+(x|X)\d{1,2})|((e|E)\d+)|((S|s)eason (\d+|I+))')
    names = filter(regex.search, fnames)

    nlist = []
    for f in names:
        nlist.append(regex.split(f)[0])
    return nlist

names = getSeries(filenames)
names = list(set(names))
names.sort()

print(names)
# keyra i gegnum lista og finna nöfn þátta út frá keyword "season"
# keyword "sxx"
# keyword "sxxexx"
# keyword "xxxx"