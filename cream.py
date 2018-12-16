import os
import re
import shutil
import sys
import tkinter
from tkinter import ttk, filedialog
from os import walk

#folder = sys.argv[1]
#target = sys.argv[2]

filenames = []
folders = []
path = []


def gui():

    root = tkinter.Tk()
    root.geometry('320x120')
    root.title('cream.py')
    
    buttonFrame = tkinter.Frame(root)
    srcFrame = tkinter.Frame(root)
    tarFrame = tkinter.Frame(root)
    src = tkinter.Label(srcFrame)
    tar = tkinter.Label(tarFrame)

    def browseSrc():
        folder = filedialog.askdirectory()
        src.config(text=folder)
    
    def browseTar():
        target = filedialog.askdirectory()
        tar.config(text=target)

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    sortButton = tkinter.Button(buttonFrame, text='Sort!')
    srcButton = tkinter.Button(srcFrame, text='Browse', command=browseSrc)
    tarButton = tkinter.Button(tarFrame, text ='Browse', command=browseTar)

    srcFrame.pack(expand=1)
    tarFrame.pack(expand=1)
    buttonFrame.pack(expand=1)
    srcButton.pack(side='left')
    tarButton.pack(side='left')
    progress.pack()
    sortButton.pack()
    src.pack(side='left')
    tar.pack(side='right')

    root.mainloop()

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
    regex = re.compile(r'((s|S)\d{1,2})|([^\d]\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))|([^\d,x,H]\d{3}([^\d,^p]|$))|(([^\d]|^)([0-1][0-8])\d{2}[^\d|^p])|(([^\d]|\d{4})[^\d](\d{1,2})\.\d{1,2}[^\d])')
    #OLD (held ég) regex = re.compile(r'((s|S)\d{1,2})|([^\d]\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))|([^\d]\d{3}([^\d|^p]|$))|(([^\d]|^)([0-1][0-8])\d{2}[^\d|^p])|(([^\d]|\d{4})[^\d](\d{1,2})\.\d{1,2}[^\d])')
    chars = ['.', '-', '[', '_']
    names = filter(regex.search, fnames)

    for f in names:
        if fileExtensions(f):
            fLow = f.lower()
            show = regex.split(f)[0]

            #   Regex if setninga helvíti -
            #   Ef season talan finnst ekki í fyrsta checki
            #   þá prufar hann næsta condition o.s.frv.
                            # S og 1-2 tölur (S02)
            season = re.findall(r's(\d{1,2})', fLow)
            if not season:  # season og 1-2 tölur
                season = re.findall(r'season (\d+)', fLow) 
            if not season:  # 1-2 tölur x og 1-2 tölur
                season = re.findall(r'[^\d](\d{1,2})x\d{1,2}[^\d]', fLow) 
            if not season:  # 1-2 tölur . og 1-2 tölur (02.05)
                season = re.findall(r'[^\d][^\d](\d{1,2})\.\d{1,2}[^\d]', fLow)
            if not season:  # 3 tölur í byrjun strengs
                season = re.findall(r'^(\d{1})\d{2}\s', fLow)
            if not season:  # 3 tölur í miðju strengs
                season = re.findall(r'[^\d,x,H](\d{1})\d{2}[^\d,p]', fLow)
            if not season: # 3 tölur í lok strengs
                season = re.findall(r'[^\d](\d{1})\d{2}$', fLow) 
            if not season:  # 4 tölur í byrjun strengs
                season = re.findall(r'^(\d{2})\d{2}\s', fLow)
            if not season:  # 4 tölur í miðju strengs, 0-1 og 0-8 svo 19xx og 20xx ártöl séu ekki mötchuð (því miður má engin sería fara yfir 19 seasons því annars kæmust öll ártöl í gegn)
                season = re.findall(r'[^\d]([0-1][0-8])\d{2}[^\d,p]', fLow)
            if not season:  # season og I+ (Season II)
                season = re.findall(r'season (i+)', fLow)
                if season: 
                    season[0] = len(season[0])

            #   Að lokum, ef ekkert tjékkið gekk, er skráin flokkuð sem "Unsorted"
            #   Season talan er formöttuð í tvo stafi (0 bætt við að framan)
            #   https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
            if not season:
                season = 'Unsorted'
            else:
                season = 'Season ' + "{:02d}".format(int(season[0]))

            #   Filter special chars úr nafninu
            #   . _ - og []
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

def makeDirs(showDic, target):
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

gui()
def Sort(folder, target):
    setLists(folder)
    makeDirs(getSeries(filenames), target)
    
#print(setLists(folder))
#print(getSeries(filenames))
#print(makeDirs(getSeries(filenames)))
#print(path)