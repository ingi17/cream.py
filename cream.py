import os
import re
import shutil
import sys
from os import walk
from pathlib import Path, PureWindowsPath

folder = sys.argv[1]
target = sys.argv[2]

filenames = []
folders = []
path = []

def setLists(folder):
    for (dirpath, dirnames, fnames) in walk(folder):
        filenames.extend(fnames)
        folders.extend(dirnames)
        
        for file in fnames:
            path.append(os.path.normpath(os.path.join(dirpath, file)))

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
    showDic = {}
    regex = re.compile(r'((s|S)\d{1,2})|(\s\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))|(^|\s)\d{2,3}(\s|[*p])')
    chars = ['.', '-', '[', '_']
    names = filter(regex.search, fnames)

    for f in names:
        if fileExtensions(f):
            
            show = regex.split(f)[0]
            season = re.findall(r's(\d{1,2})', f.lower())

            if season:
                #season = 'Season ' + season[0]
                season = 'Season ' + "{:02d}".format(int(season[0]))#https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
            else:
                season = 'Unsorted'

            for c in chars:
                show = show.replace(c, ' ')
                show = re.sub('  +', ' ', show)
            
            show = show.lower().strip()
            show = show.title()
            
            if show not in showDic:
                showDic[show] = {}
                if season:
                    showDic[show][season] = [f]
                else:
                    showDic[show] = [f]
            
            elif show in showDic:
                showDic[show]
                if season not in showDic[show]:
                    showDic[show][season] = [f]
                elif f not in showDic[show][season]:
                    showDic[show][season].append(f)

    dictToTxt(showDic)

    return showDic

def makeDirs(showDic):
    if not os.path.exists(target):
        os.makedirs(target)

    for key in showDic:

        dirs = target + '/' + key


        if not os.path.exists(dirs):
            os.makedirs(dirs)

        for keykey in showDic[key]:
            dirSeason = dirs + '/' + keykey

            if not os.path.exists(dirSeason):
                os.makedirs(dirSeason)

            for show in showDic[key][keykey]:
                for i in path:
                    if show in i:
                        try:
                            #shutil.move(i, dirSeason)
                            shutil.copy(i, dirSeason)
                        except Exception as ex:
                            print(ex)
                                    
def dictToTxt(dicto):
    with open('dictListi.txt', 'w') as file:
        for k, v in dicto.items():
            file.write(str(k) + ' >>> '+ str(v) + '\n\n')

def listToTxt(listo):
    with open('keyListi.txt', 'w') as file:
        for k in listo:
            for kk in listo[k]:
                file.write(k + '>>' + kk + '\n\n')

print(setLists(folder))
#print(getSeries(filenames))
print(makeDirs(getSeries(filenames)))
#print(path)
