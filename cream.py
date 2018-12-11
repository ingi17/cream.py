import sys
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
    names = []
    for f in fnames:
        keyword = "s0"
        if keyword in f.lower():
            names.append(f.lower().split(keyword,1)[0])
        
        keyword = "s1"
        if keyword in f.lower():
            names.append(f.lower().split(keyword,1)[0])

        keyword = "season"
        if keyword in f.lower():
            names.append(f.lower().split(keyword,1)[0])
    return names

names = getSeries(filenames)
names = list(set(names))

print(names)
# keyra i gegnum lista og finna nöfn þátta út frá keyword "season"
# keyword "sxx"
# keyword "sxxexx"
# keyword "xxxx"