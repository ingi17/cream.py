import sys
import re
from os import walk

folder = sys.argv[1]
target = sys.argv[2]

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
<<<<<<< HEAD
    regex = re.compile('((s|S)\d{1,2})|(\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))')
=======
    regex = re.compile(r'((s|S)\d+)|(\d+(x|X)\d{1,2})|((e|E)\d+)|((S|s)eason (\d+|I+))')
>>>>>>> 2a5713574fe8cef143e7f37c052c2af52da6238f
    names = filter(regex.search, fnames)

    nlist = []
    chars = ['.', '-', '[']
    for f in names:
<<<<<<< HEAD
        show = regex.split(f)[0]

        for c in chars:
            show = show.replace(c, ' ')

        nlist.append(show.strip())

    shows = list(set(nlist))
    shows.sort()

    return shows

print(getSeries(filenames))


def makeDirs():
    return 0


=======
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
>>>>>>> 2a5713574fe8cef143e7f37c052c2af52da6238f
# keyra i gegnum lista og finna nöfn þátta út frá keyword "season"
# keyword "sxx"
# keyword "sxxexx"
# keyword "xxxx"