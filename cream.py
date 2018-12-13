import sys, re, os
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

def fileExtensions(file):
    if re.search(r'(s|S)ample', file):
        return False
    elif re.search(r'.mkv$|.flv$|.avi$|.wmv$|.mov$|.mp4$|.mpg$|.mpeg$|.nfv$|.mp3$', file):
        return True
    return False
    #if re.search(r'.png$|.dat$|.nfo$|.jpg$|.url$|.URL$|.txt$|(s|S)ample', file):
     #   return False
    #return True

def getSeries(fnames):
    regex = re.compile(r'((s|S)\d{1,2})|(\s\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))|(^|\s)\d{2,3}(\s|[*p])')
    names = filter(regex.search, fnames)

    nlist = []
    chars = ['.', '-', '[', '_']

    for f in names:
        if fileExtensions(f):
            show = regex.split(f)[0]
            for c in chars:
                show = show.replace(c, ' ')
            show = show.lower()
            show = show.title()
            nlist.append(show.strip())

    shows = list(set(filter(None, nlist)))
    shows.sort()
    print(len(shows))
    return shows

def makeDirs(shows):
    if not os.path.exists(target):
        os.makedirs(target)

    for show in shows:
        dirs = target + "/" + show + "/"
        if not os.path.exists(dirs):
            os.makedirs(dirs)

setLists(folder)
print(getSeries(filenames))
#makeDirs(getSeries(filenames))
