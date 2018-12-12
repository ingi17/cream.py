import sys
import re
from os import walk

folder = sys.argv[1]
target = sys.argv[2]

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
    regex = re.compile('((s|S)\d{1,2})|(\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))')
    names = filter(regex.search, fnames)

    nlist = []
    chars = ['.', '-', '[']
    for f in names:
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


# keyra i gegnum lista og finna nöfn þátta út frá keyword "season"
# keyword "sxx"
# keyword "sxxexx"
# keyword "xxxx"