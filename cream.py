import sys, re, os, shutil
from os import walk

folder = sys.argv[1]
target = sys.argv[2]

filenames = []
folders = []
path = []
dictoTest = {}

def setLists(folder):
    for (dirpath, dirnames, fnames) in walk(folder):
        filenames.extend(fnames)
        folders.extend(dirnames)
        path.append(dirpath)

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
                show = re.sub('  +', ' ', show)
            show = show.lower().strip()
            show = show.title()
            if show not in dictoTest:
                dictoTest[show] = [f]
            elif show in dictoTest:
                if f not in dictoTest[show]:
                    dictoTest[show].append(f) 
            nlist.append(show.strip())
    shows = list(set(filter(None, nlist)))
    shows.sort()
    #print(len(shows))
    dictToTxt(dictoTest)
    listToTxt(dictoTest)
    return dictoTest
    #return shows

def makeDirs(shows):
    print(path[5])
    if not os.path.exists(target):
        os.makedirs(target)

    for key in dictoTest:
        dirs = target + "/" + key + "/"
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            #for i in dictoTest[key]:
                #if i in path:
                    #shutil.move(, dirs)

def dictToTxt(dicto):
    with open('dictListi.txt', 'w') as file:
        for k, v in dicto.items():
            file.write(str(k) + ' >>> '+ str(v) + '\n\n')

def listToTxt(listo):
    with open('keyListi.txt', 'w') as file:
        for k in listo:
            file.write(k + '\n\n')
setLists(folder)
print(getSeries(filenames))
makeDirs(getSeries(filenames))
