import os
import re
import shutil
import sys
import tkinter
from tkinter import ttk, filedialog
from os import walk

#   sys.argv skipanir commentaðar þar sem við ákváðum að henda í eitt stk GUI frekar en að hafa skriptuna með source og target filepath með í skipuninni.
#   UNCOMMENT FOR python cream.py /path/to/download/folder /path/to/structured/folder
#folder = sys.argv[1]
#target = sys.argv[2]

filenames = []
folders = []
path = []

#   SetLists nýtir os.walk til að skrá öll filenames, folders og paths í sér lista
def setLists(folder):
    for (dirpath, dirnames, fnames) in walk(folder):
        filenames.extend(fnames)
        folders.extend(dirnames)
        
        for file in fnames:
            path.append(os.path.normpath(os.path.join(dirpath, file)))

#   fileExtensions er nýtt með regex til að hunsa allar skráarendingar sem eru ekki mynd eða hljóð file-ar
#   Auk þess viljum við ekki sample skrár
def fileExtensions(file):
    if re.search(r'(s|S)ample', file):
        return False
    elif re.search(r'.mkv$|.flv$|.avi$|.wmv$|.mov$|.mp4$|.mpg$|.mpeg$|.nfv$|.mp3$', file):
        return True
    return False

    # Gamalt regex sem matchaði endingar sem við vildum ekki.
    # - Deprecated í stað fyrir regexið fyrir ofan sem matchar aðeins það sem við viljum.

    #if re.search(r'.png$|.dat$|.nfo$|.jpg$|.url$|.URL$|.txt$|(s|S)ample', file):
     #   return False
    #return True

def getSeries(fnames):
    #   showDic = SHOW >>> {'SEASON': ['EPISODE FILENAME']}
    showDic = {}
    
    #   Regex til að matcha við _ALLAR HELSTU_ týpur af Season nöfnum í skrám (Season 00, 00x00, S00E00, 00.00)
    regex = re.compile(r'((s|S)\d{1,2})|([^\d]\d{1,2}(x|X)\d{1,2})|((e|E)\d{1,2})|((S|s)eason (\d+|I+))|([^\d,x,H]\d{3}([^\d,^p]|$))|(([^\d]|^)([0-1][0-8])\d{2}[^\d|^p])|(([^\d]|\d{4})[^\d](\d{1,2})\.\d{1,2}[^\d])')
    #   Notum filter til að minnka settið sem við vinnum úr. Allar skrár 
    names = filter(regex.search, fnames)

    #   Special characters til að tæma úr streng sem er notaður fyrir þáttarnafn
    chars = ['.', '-', '[', '_']

    for f in names:
        if fileExtensions(f):

            fLow = f.lower()

            #   Þáttarnafn generateað frá fyrsta staki, eftir split á Season í filenafni
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
            
            #   Athugar hvort þáttarnafnið sé til og býr þá til key í dictið
            if show not in showDic:
                showDic[show] = {}
                #   Ef season nafnið fannst þá búum við til dict inn í dict með Þáttarnafninu >>> Season XX
                if season:
                    showDic[show][season] = [f]
                else:
                    showDic[show] = [f]
            
            #   Ef þátturinn er núþegar til sem key í showDic, ef season lykillinn er ekki fundinn þá er hann búinn til annars stakinu bætt við undir
            elif show in showDic:
                if season not in showDic[show]:
                    showDic[show][season] = [f]
                elif f not in showDic[show][season]:
                    showDic[show][season].append(f)

    return showDic

def makeDirs(showDic, target):
    if not os.path.exists(target):
        os.makedirs(target)

    #   Lykkja sem býr til möppu út frá efsta lykli í dict.
    #   Býr s.s. til þáttarnafns möppurnar.
    for key in showDic:

        dirs = target + '/' + key

        if not os.path.exists(dirs):
            os.makedirs(dirs)

        #   Fyrir hvern lykil (season) undir efsta lykil (þáttur).
        #   - Path skapað og season mappa sköpuð
        for keykey in showDic[key]:
            dirSeason = dirs + '/' + keykey

            if not os.path.exists(dirSeason):
                os.makedirs(dirSeason)

            #   Fyrir hvert einasta stak undir þætti >>> season
            #   Borið saman við heildar path listann sem var skapaður í byrjun
            #   Ef pathið finnst þá er skráin færð yfir í viðeigandi möppu undir þáttur >>> season
            for show in showDic[key][keykey]:
                for i in path:
                    if show in i:
                        try:
                            #   Move skilar villum á nokkrum ákveðnum skrám sem við því miður gerðum ekki ráð fyrir
                            #   Forritið virkar villulaust með copy. Ekki guðmund hvers vegna :'(
                            shutil.move(i, dirSeason)
                            #shutil.copy(i, dirSeason) # Copy frekar en move fyrir dev testing
                        except Exception as ex:
                            print(ex)
                                    
def dictToTxt(dicto):
    with open('dictListi.txt', 'w') as file:
        for k, v in dicto.items():
            file.write(str(k) + ' >>> '+ str(v) + '\n\n')

#   GUI gert með tkinter.
#   Smá skítamix þurfti til að koma variables frá browse tökkum yfir í parameter fyrir sort föll, þess vegna liggja globals hérna fyrir neðan

global folder
global target

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
        folder.set(filedialog.askdirectory())
        src.config(text=folder.get())
        progress['value']=10
    
    def browseTar():
        target.set(filedialog.askdirectory())
        tar.config(text=target.get())
        progress['value']=20

    def Sort(source, dest):
        progress['value']=50
        print(source, dest)
        setLists(source)
        progress['value']=75
        makeDirs(getSeries(filenames), dest)
        progress['value']=100

    progress = ttk.Progressbar(root, length=300, mode='determinate')
    target = tkinter.StringVar()
    folder = tkinter.StringVar()
    sortButton = tkinter.Button(buttonFrame, text='Sort!', command= lambda: Sort(folder.get(), target.get()))
    srcButton = tkinter.Button(srcFrame, text='Source', command=browseSrc)
    tarButton = tkinter.Button(tarFrame, text ='Target', command=browseTar)

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

gui()

#---Gömul virkni fyrir skriptu án GUI
#--- UNCOMMENT FOR python cream.py /path/to/download/folder /path/to/structured/folder
# setLists(folder)
# makeDirs(getSeries(filenames), target)