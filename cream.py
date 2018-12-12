import sys
import re
from os import walk

folder = sys.argv[1]
#target = sys.argv[2]

filenames = []
folders = []
path = []

def setLists(folder):
    for (dirpath, dirnames, fnames) in walk(folder):
        filenames.extend(fnames)
        folders.extend(dirnames)
        path.append(dirpath)

setLists(folder)
def ingoreFiles(file):
    if re.search(r'.png$|.dat$|.nfo$|.jpg$|.url$|.URL$|.txt$|(s|S)ample', file):
        return False
    return True

def getSeries(fnames):
    regex = re.compile(r'((s|S)\d+)|(\d+(x|X)\d{1,2})|((e|E)\d+)|((S|s)eason (\d+|I+))')
    names = filter(regex.search, fnames)

    nlist = []
    for f in names:
        #print(f)
        #if re.search('.png$|.dat$|.nfo$|.jpg$|.url$|.URL$|.txt$|(s|S)ample', f):
         #   pass
        #else:
        if ingoreFiles(f):
            nlist.append(regex.split(f)[0])
    return nlist

names = getSeries(filenames)
names = list(set(names))
names.sort()
#for i in names:
 #   print(i)
print(names)
# keyra i gegnum lista og finna nöfn þátta út frá keyword "season"
# keyword "sxx"
# keyword "sxxexx"
# keyword "xxxx"