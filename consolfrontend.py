#Frontend for usage of Project Mimir in Terminal
# MTF (MimirTerminalFrontend) v0.4.0
#2014-2015, K. Schweiger
import backend
import missingspecs
import os
import random
import time
import MTFconfig
import sharedfunctions
from operator import itemgetter
import colorprinting
import sys

#define width of the terminal window
def getwidth():
    return 140

#define height of the terminal window
def getheight():
    return 43

#function, to generate a string of a LENGHTS, that contains only SYMBOL
def makestring(symbol, lengths):
    string = ""
    for i in range(0,lengths):
        string = string + symbol
    return string

def banner(database):
    print makestring("-",getwidth())
    print makestring("-",(getwidth()/2)-11)+" Project Mimir "+backend.getVersion()+" "+makestring("-",(getwidth()/2)-11)
    print makestring("-",getwidth())
    print "-"+makestring(" ",getwidth()-2)+"-"
    print "-"+makestring(" ",7)+"Code | Name                 | Comments                                                                                             -"
    print "-"+makestring(" ",7)+"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++      -"
    print "-"+makestring(" ",7)+"   0 | Exit                 |                                                                                                      -"
    print "-"+makestring(" ",7)+"   1 | Execute              | Opens the selected Entry in an external Applicatiom                                                  -"
    print "-"+makestring(" ",7)+"   2 | Modify               | Modify Name, Genres, Interprets, Studio and Rating. Genres and Interprets are Lists, so you          -"
    print "-"+makestring(" ",12)+    " "+makestring(" ",22)+"| can Append and Modify Elements or overwrite the list                                                 -"
    print "-"+makestring(" ",7)+"   3 | Print Information    | Prints the informations of a given entry (Input: ID)                                                 -"
    print "-"+makestring(" ",7)+"   4 | Random !!!!          | Execute a Random Entry. If printed by criteria, execute one of these                                 -"
    print "-"+makestring(" ",7)+"   5 | Statistics           | Choose between different statistics                                                                  -"
    print "-"+makestring(" ",7)+"  42 | Help                 | Get a few informations and help                                                                      -"
    print "-"+makestring(" ",7)+"  99 | DB options           | Options for modifieing the DB                                                                        -"
    print "-"+makestring(" ",getwidth()-2)+"-"
    print "- "+str(database)+makestring(" ",getwidth()-14-len(database))+"MTF v0.5.0 -"
    print makestring("-",getwidth())

def intinput(string):
    flag = False
    while flag == False:
        try:
            input = int(raw_input(string))
            flag = True
        except ValueError:
            print "The input requires to be an integer"
            flag = False
    return input

def DBoptions(DB, DBexists, directory):
    print "+---+-------Options------------------+"
    print "| 1 | Create new DB                  |"
    print "| 2 | Read existing DB               |"
    print "| 3 | Remove Entrys/Find new Fils    |"
    print "| 4 | Check for changed Directorys   |"
    print "| 5 | Save DB                        |"
    print "| 6 | Add new specs to the DB        |"
    print "| 7 | Remove a File                  |"
    print "+---+--------------------------------+"
    Code = intinput("Choose Mode: ")
    if Code == 1:
        if DBexists == False:
            directory = raw_input('Input starting directory:')
            DB = backend.database(0,directory)
            DBexists = True
        else:
            print "There is already a Database"
            raw_input('Input anything to go on')
    elif Code == 2:
        if DBexists == False:
            ignore = False
            directory = raw_input('Input directory where database file is located: ')
            DB = backend.database(1,directory)
            if DB.worked == False:
                raw_input("Please press a key")
                ignore = True
            else:
                DBexists = True
        else:
            print "There is already a Database"
            raw_input('Input anything to go on')
    elif Code == 3:
        if DBexists == True:
            removeentrys(DB)
        else:
            print "There is no DB yet"
    elif Code == 4:
        if DBexists == True:
            #searchnewfiles(DB)
            changeddirs(DB,directory)
        else:
            print "There is no DB yet"
    elif Code == 5:
        if DBexists == True:
            sharedfunctions.backupfile(directory, 'main.db')
            DB.saveDB()
        else:
            print "There is no DB yet"
    elif Code == 6:
        if DBexists == True:
            missingspecs.main(directory)
            del DB
            DB = backend.database(1,directory)
        else:
            print "There is no DB yet"
    elif Code == 7:
        if DBexists == True:
            rmid = intinput("Input ID of Entry, that should be removed from the filesystem: ")
            path = DB.entrys[rmid].getSpec("PATH")
            print "\nYou want to remove:"
            printaentry2(DB, True, rmid)
            print ""
            sharedfunctions.removefile(path)
        else:
            print "There is no DB yet"
    else:
        print "Wront input"
    return DBexists


#make nice listings Specs, when printing enrys with the printentrys function
def findmaxSpeclen(DB, IDlist, specname):
    #find longest Spec
    maxSpeclen = 0
    maxSinglelen = []
    maxlenid = 0
    NLen = MTFconfig.getconfigpart("/home/korbi/Code/ProjectMimir/", "MaxNameLen")
    DAcc = MTFconfig.getconfigpart("/home/korbi/Code/ProjectMimir/", "DateAcc")
    for i in IDlist:
        tmpSinglelen = []
        spec = DB.entrys[i].getSpec(specname)
        #print spec
        #if the spec is als list find combined lengths of alle entrys in the list
        if type(spec) is list:
            comblen = 0
            secen = False
            for e in spec:
                #print e
                if e != "nogenre" and e != 'nointerpret' and e != "nostudio":
                    if secen == True:
                        comblen = comblen + 1
                    comblen = comblen + len(e)
                    tmpSinglelen.append(len(e))
                    secen = True
            tmplen = comblen
        #if the spec is no list, just get lengths of the spec
        else:
            #print spec
            tmplen = len(spec)
            if specname == "NAME":
                #print "hallo"
                #print tmplen
                tmplen = NLen
            if specname == "OPENED":
                if DAcc == "short":
                    tmplen = 8
            #print tmplen
        #look if the spec is the longest
        if tmplen > maxSpeclen:
            maxSpeclen = tmplen
            maxlenid = i
            maxSinglelen = tmpSinglelen
    maxlenlist = [maxSpeclen]
    maxlenlist = maxlenlist + maxSinglelen
    #print "maxlenlist: "
    #print maxlenlist
    return  maxlenlist



def execute(DB):
    idtoexecute = int(raw_input('Input ID of entry, to be executed: '))
    if idtoexecute == -1:
       idtoexecute = random.randint(0, DB.getnumberofentrys())
    print "Now playing:",DB.entrys[idtoexecute].getSpec("NAME")
    DB.runentry(idtoexecute)
    DB.entryopened(idtoexecute)

def executeranlist(DB, idlist, played):
    if idlist == "all":
        idtoexecute = random.randint(0, DB.getnumberofentrys())
        printaentry2(DB, True, idtoexecute)
        DB.runentry(idtoexecute)
        DB.entryopened(idtoexecute)
    else:
        playedflag = False
        while(playedflag == False):
            listentry = random.randint(0, len(idlist)-1)
            if listentry not in played:
                playedflag = True
        printaentry2(DB, True, idlist[listentry])
        DB.runentry(idlist[listentry])
        DB.entryopened(idlist[listentry])
        return listentry

def searchnewfiles(DB):
    directory = raw_input('Input directory where database file is located:')
    DB.findnewfiles(directory)


def changeddirs(DB, StartDir):
    changed = DB.changedpaths(StartDir)
    for i in range(len(changed)):
                print colorprinting.blue(changed[i][0])," was at ", colorprinting.red(changed[i][1])," and is now at ",colorprinting.green(changed[i][2])
    raw_input('press anything')

def getentrysbydate(DB,flag,num):
    flaglist = ["LASTMOD","ADDED","OPENED"]
    numtolist = num
    date = [00,00,00,00,00,00]
    order = [2,1,0,3,4,5]
    numofentrys = DB.getnumberofentrys()
    idlist = []
    if flag in flaglist:
        for i in range(numtolist):
            #print "i = ",i
            #raw_input("press1")
            date = [00,00,00,00,00,00]
            for j in range(0,numofentrys):
                #print "j = ",j
                #if j%100 == 1:
                    #raw_input("press")
                if j in idlist:
                    machwas = 0
#                    date = [00,00,00,00,00,00]
                else:
                    #if True:
                    if flag == "OPENED" and DB.entrys[j].getSpec("OPENED") != "neveropened" or flag == "LASTMOD" and DB.entrys[j].getSpec("LASTMOD") != "nevermod" or flag == "ADDED":
                        entrydate = []
                        newdate = False
                        tmp1 = DB.entrys[j].getSpec(flag).split("|")
                        entrydate = entrydate + tmp1[0].split(".")
                        entrydate = entrydate + tmp1[1].split(":")
                        #print entrydate
                        for position in order:
                            lowflag = True
                            if int(entrydate[position]) > int(date[position]):
                                for k in order:
                                    if k == position:
                                        #print "k = ",k
                                        break
                                    else:
                                        if date[k] > entrydate[k]:
                                            #print "Tatu"
                                            lowflag = False
                                if lowflag == True:
                                    date = entrydate
                                    newid = DB.entrys[j].getSpec("ID")
                                    newdate = True
                                    #print "newid = ", newid
                                #print entrydate," --- ",date
            idlist.append(int(newid))
    return idlist


def printaentry2(DB,execflag, execid = None):
    execflag = 1
    if execid != None:
        if execflag == True:
            mode = 0
    else:
        played = []
        print "Printing Mode"
        jump = False
        criteriaprint = False
        print "+---+--------------------------+"
        print "| 1 | Single entry             |"
        print "| 2 | Range of entrys          |"
        print "| 3 | Print by criteria        |"
        print "| 4 | Print all                |"
        print "| 5 | Print by Date Added      |"
        print "| 6 | Print by Date Modified   |"
        print "| 7 | Print by Date Opened     |"
        print "+---+--------------------------+"
        mode = intinput('Choose Mode: ')
    if mode == 0:
        startid = int(execid)
        idlist = [startid]
        jump = True
        execflag = 0
    elif mode == 1:
        startid = int(raw_input('Input first ID of range: '))
        idlist = [startid]
        jump = True
        #raw_input('Input anything to go on')
    elif mode == 2:
        startid = int(raw_input('Input first ID of range: '))
        endid = int(raw_input('Input last ID of range: '))
        idlist = range(startid,endid+1)
        jump = True
    elif mode == 3:
        print "Print by Criteria"
        criteriastr = raw_input('Type criteria seperated by spaces: ')
        criterialist = criteriastr.split(" ")
        idlist =  DB.listbycriteria(criterialist)
        jump = True
        criteriaprint = True
    elif mode == 4:
        idlist =  DB.listbycriteria([])
        jump = True
    elif mode == 5:
        idlist = getentrysbydate(DB,"ADDED",15)
        jump = True
    elif mode == 6:
        idlist = getentrysbydate(DB,"LASTMOD",15)
        jump = True
    elif mode == 7:
        idlist = getentrysbydate(DB,"OPENED",15)
        jump = True

    else:
        jump = False
    #Code for nice printing
    if jump == True:
        SpecstoPrint = ["GENRE","INTERPRET","STUDIO","NUMOPENED","OPENED"]
        SpecsPrinted = ["GENRE","INTERPRET","STUDIO","#","OPENED"]
        lengths = []
        for spec in SpecstoPrint:
            lengths.append(findmaxSpeclen(DB,idlist,spec))
        if lengths[0][0] <= 5:
            lengths[0][0] = 5
        if lengths[1][0] <= 9:
            lengths[1][0] = 9
        if lengths[2][0] <= 6:
            lengths[2][0] = 6
        lengths[4][0] = 8
        #print lengths
        header =  "ID"+makestring(" ",3)+"NAME"+makestring(" ",17)
        subheader = makestring("-",3)+makestring(" ",2)+makestring("-",21)+makestring("+",1)
        for i in range(len(lengths)):
            if lengths[i][0] != 0:
                header = header+"|"+SpecsPrinted[i]+makestring(" ",lengths[i][0]-len(SpecsPrinted[i]))
                subheader = subheader + makestring("-",lengths[i][0])+makestring("+",1)
        print header
        print subheader
#        print lengths[3][0]
        for i in idlist:
            #DB.entrys[i].printentry(lengths)
            if int(DB.entrys[i].id) <= 9:
                idprint = "  "+str(DB.entrys[i].id)
            elif int(DB.entrys[i].id) <= 99 and int(DB.entrys[i].id) > 9:
                idprint = " "+str(DB.entrys[i].id)
            elif int(DB.entrys[i].id) >= 100:
                idprint = str(DB.entrys[i].id)
            if len(DB.entrys[i].name) >= 20:
                nameprint = DB.entrys[i].name[0:19]+".."
            elif len(DB.entrys[i].name) < 20:
                nameprint = DB.entrys[i].name +(21-len(DB.entrys[i].name))*(" ")
            #Define what is shown:
            genreflag = False
            interpretflag = False
            studioflag = False
            openedflag = False
            numflag = False
            genreprint = []
            for genre in DB.entrys[i].genre:
                if genre != "nogenre":
                    genreprint.append(genre)
                    genreflag = True
            interpretprint = []
            for interpret in DB.entrys[i].interpret:
                if interpret != "nointerpret":
                    interpretprint.append(interpret)
                    interpretflag = True
            studioprint = ""
            if DB.entrys[i].studio != "nostudio":
                studioprint = DB.entrys[i].studio
                studioflag = True
            openedprint = ""
            if DB.entrys[i].opened != "neveropened":
                openedprint = DB.entrys[i].opened[0:8]
                openedflag = True
            numprint = ""
            numprint = DB.entrys[i].numopened
            if int(numprint) <= 9 and lengths[3][0] > 1:
                numprint = " "+numprint
            numflag = True
            if lengths == None:
                printedstring = idprint+"  "+nameprint+"  "
                if genreflag == True:
                    printedstring = printedstring+" "+' '.join(genreprint)
                if interpretflag == True:
                    printedstring = printedstring+" "+(' '.join(interpretprint)).replace("%"," ")
                if studioflag == True:
                    printedstring = printedstring+" "+studioprint
                if openedflag == True:
                    printedstring = printedstring+" "+openedprint
            else:
                printedstring = idprint+"  "+nameprint
                printedgenre = ""
                printedinterpret = ""
                printedstudio = ""
                printedopened = ""
                printednum = ""
                if genreflag == True:
                    i = -1
                    glen = 0
                    firstflag = True
                    for g in genreprint:
                        if firstflag == True:
                            printedgenre = printedgenre + "|"  + g
                            firstflag = False
                        else:
                            printedgenre = printedgenre + " "  + g
                        glen = glen + len(g)
                        i = i + 1
                    glen = glen + i
                    #print glen, i
                    if glen < lengths[0][0]:
                        printedgenre = printedgenre + makestring(" ",lengths[0][0]-glen)
                if genreflag == False:
                    printedgenre = "|" +  makestring(" ",lengths[0][0])
                printedstring = printedstring + printedgenre
                if interpretflag == True:
                    i = -1
                    firstflag = True
                    ilen = 0
                    for inter in interpretprint:
                        if firstflag == True:
                            printedinterpret = printedinterpret + "|" + inter.replace("%"," ")
                            firstflag = False
                        else:
                            printedinterpret = printedinterpret + " " + inter.replace("%"," ")
                        ilen = ilen + len(inter)
                        i = i + 1
                    ilen = ilen + i
                    if ilen < lengths[1][0]:
                        printedinterpret = printedinterpret + makestring(" ",lengths[1][0]-ilen)
                if interpretflag == False:
                    printedinterpret = "|" + makestring(" ",lengths[1][0])
                printedstring = printedstring + printedinterpret
                if studioflag == True:
                    printedstudio = "|" + studioprint + makestring(" ",lengths[2][0]-len(studioprint))
                if studioflag == False:
                    printedstudio = "|" + makestring(" ",lengths[2][0])
                printedstring = printedstring + printedstudio
                if numflag == True:
                    printednum = "|"+numprint +makestring(" ",lengths[3][0]-len(numprint))
                printedstring = printedstring + printednum
                if openedflag == True:
                    printedopened = "|" + openedprint + makestring(" ",lengths[4][0]-len(openedprint))
                if openedflag == False:
                    printedopened = "|" + makestring(" ",lengths[4][0])
                printedstring = printedstring + printedopened
            print printedstring
        #raw_input('Input anything to go on')
    else:
        raw_input('Invalid Mode. Press key to continue')
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            printaentry2(DB, False, None)
#            flag = printaentry2(DB)
        if execflag == 4:
            #if criteriaprint == True:
            ranid = executeranlist(DB, idlist, played)
            played.append(ranid)
            if len(played) == len(idlist):
                played = []
            #else:
            #    executeranlist(DB, "all")
        if execflag == 0:
            return False
        if flag == False:
            break

def advancedprinting(DB, workdir):
    execflag = 1
    #Idea for the advanced printing function
    #1) Define the id's to be printed
    print "+---+--------------------------+"
    print "| 1 | Single entry             |"
    print "| 2 | Range of entrys          |"
    print "| 3 | Print by criteria        |"
    print "| 4 | Print all                |"
    print "| 5 | Print by Date Added      |"
    print "| 6 | Print by Date Modified   |"
    print "| 7 | Print by Date Opened     |"
    print "+---+--------------------------+"
    mode = intinput('Choose Mode: ')
    #   1.1) Print single/range/all entrys
    if mode == 1 or mode == 2 or mode == 4:
        jump = False
        idlist = []
        if mode != 4:
            idlist.append(intinput("(First) ID to be printed: "))
            if mode == 2:
                for i in range(idlist[0]+1, intinput("Last ID to be printed: ")+1):
                    idlist.append(i)
        #Print all:
        if len(idlist) == 0:
            idlist =  DB.listbycriteria([]) #return a list with all ID's
        #Now you got the list idlist, that has 1, all ID's between two given ID's or all ID's inside
    #   1.2) Print by criteria
    if mode == 3:
        jump = False
        criterianum = intinput('Input the number of criteria: ')
        criteriastr = raw_input('Type criteria seperated by spaces: ')
        criterialist = criteriastr.split(" ")
        idlist =  DB.listbycriteria(criterialist)
    #   1.3) print by Dates
    if mode == 5 or mode == 6 or mode == 7:
        jump = False
        numtoprint = MTFconfig.getconfigpart(workdir, "NumToPrint")
        if mode == 5:
            printby = "ADDED"
        if mode == 6:
            printby = "LASTMOD"
        if mode == 7:
            printby = "OPENED"
        idlist = getentrysbydate(DB,printby,numtoprint)
    if mode == 0:
        jump = True
        execflag = 0
    if jump == False:
        played = []
        #2) Get from config, what should be printed
        #In the MTFconfig module all operations on the config are defined. getconfigpart(dir,cfg)
        #retuns a list corresponting to cfg.
        pSpecs = MTFconfig.getconfigpart("/home/korbi/Code/ProjectMimir/", "SpecsToPrint")
        sSpecs = MTFconfig.getconfigpart("/home/korbi/Code/ProjectMimir/", "SpecsToShow")
        NLen = MTFconfig.getconfigpart("/home/korbi/Code/ProjectMimir/", "MaxNameLen")
        #find maximal length of printed specs
        lengths = []
        for spec in pSpecs:
            #print spec
            tmplen = findmaxSpeclen(DB,idlist,spec)
            lengths.append(tmplen)
        for i in range(len(pSpecs)):
            if lengths[i][0] <= len(sSpecs[i]):
                lengths[i][0] = len(sSpecs[i])
        #print lengths
        #3) Generate Header
        header = ""
        subheader = ""
        for i in range(len(lengths)):
            header = header + sSpecs[i]+makestring(" ",lengths[i][0]-len(sSpecs[i]))+makestring("|",1)
            subheader = subheader + makestring("-",lengths[i][0])+makestring("+",1)
        print header
        print subheader
        #4) Print each entry with the in the config defined specs
        for i in idlist:
            tmpline = ""
            for spec in pSpecs:
                if spec == "ID":
                    if int(DB.entrys[i].id) <= 9:
                        tmpline = tmpline + makestring(" ",2) +str(DB.entrys[i].id)
                    elif int(DB.entrys[i].id) <= 99 and int(DB.entrys[i].id) > 9:
                        tmpline = tmpline + makestring(" ",1) +str(DB.entrys[i].id)
                    elif int(DB.entrys[i].id) >= 100:
                        tmpline = tmpline + str(DB.entrys[i].id)
                elif spec == "NAME":
                    name = DB.entrys[i].name
                    if len(name) > NLen:
                        tmpline = tmpline + name[0:NLen-2] + makestring(".",2)
                    else:
                        tmpline = tmpline + name + makestring(" ",NLen - len(name))
                elif spec == "GENRE":
                    for k in range(len(lengths)):
                        if pSpecs[k] == "GENRE":
                            maxlen = lengths[k][0]
                    genrelist = []
                    for genre in DB.entrys[i].genre:
                        if genre != "nogenre":
                            genrelist.append(genre)
                    if len(genrelist) == 0:
                            tmpline = tmpline + makestring(" ",maxlen)
                    else:
                        a1 = 0
                        for genre in genrelist:
                            a1 = a1 + len(genre + makestring(" ",1))
                            tmpline = tmpline + genre + makestring(" ",1)
                        tmpline = tmpline + makestring(" ",maxlen-a1)
                    if a1 > maxlen:
                        tmpline = tmpline[:-1]
                elif spec == "INTERPRET":
                    for k in range(len(lengths)):
                        if pSpecs[k] == "INTERPRET":
                            maxlen = lengths[k][0]
                    interpretlist = []
                    for interpret in DB.entrys[i].interpret:
                        if interpret != "nointerpret":
                            interpretlist.append(interpret)
                    if len(interpretlist) == 0:
                            tmpline = tmpline + makestring(" ",maxlen)
                    else:
                        a1 = 0
                        for interpret in interpretlist:
                            a1 = a1 + len(interpret.replace("%"," ") + makestring(" ",1))
                            tmpline = tmpline + interpret.replace("%"," ") + makestring(" ",1)
                        tmpline = tmpline + makestring(" ",maxlen-a1)
                    if a1 > maxlen:
                        tmpline = tmpline[:-1]
                elif spec == "STUDIO":
                    for k in range(len(lengths)):
                        if pSpecs[k] == "STUDIO":
                            maxlen = lengths[k][0]
                    tmpline = tmpline + DB.entrys[i].studio + makestring(" ",maxlen - len(DB.entrys[i].studio))
                elif spec == "NUMOPENED":
                    for k in range(len(lengths)):
                        if pSpecs[k] == "NUMOPENED":
                            maxlen = lengths[k][0]
                    tmpline = tmpline + DB.entrys[i].numopened + makestring(" ",maxlen - len(DB.entrys[i].numopened))
                elif spec == "OPENED":
                    for k in range(len(lengths)):
                        if pSpecs[k] == "OPENED":
                            maxlen = lengths[k][0]
                    date = DB.entrys[i].opened
                    if date == "neveropened":
                        tmpline = tmpline + makestring(" ",maxlen)
                    else:
                        tmpline = tmpline + date[0:8] + makestring(" ",maxlen - len(date[0:8]))
                tmpline = tmpline + makestring("|",1)
            print tmpline
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            advancedprinting(DB, "")
#            flag = printaentry2(DB)
        if execflag == 4:
            #if criteriaprint == True:
            ranid = executeranlist(DB, idlist, played)
            played.append(ranid)
            if len(played) == len(idlist):
                played = []
            #else:
            #    executeranlist(DB, "all")
        if execflag == 0:
            return False
        if flag == False:
            break



def modifyaentry(DB):
    print "Modifying Mode"
    mode = intinput('Mode? (1: Single entry, 2: Range of entrys, 3: List of entrys, 4: Single entry multiple times, 5: Change per Interpret) ')
    if mode == 1:
        entryid = intinput('Input ID of entry to modify: ')
        spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET): ')
        if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
            newspec = raw_input('Input the new value of the choosen spec: ')
            DB.modifyentry(spec, newspec, entryid)
        elif spec == "GENRE" or spec == "INTERPRET":
            changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW, CHANGE)? ')
            if changehow == "APPEND" or changehow == "NEW":
                newspec = raw_input('Input the new value of the choosen spec: ')
                if spec == "INTERPRET":
                    newspec = newspec.replace(" ","%")
                DB.modifyentry(spec, newspec, entryid, None, changehow)
            elif changehow == "CHANGE":
                newspec = raw_input('Input the new value of the choosen spec: ')
                if spec == "INTERPRET":
                    newspec = newspec.replace(" ", "%")
                listnum = intinput('Input the index you what to change in the speclist: ')
                DB.modifyentry(spec,newspec, entryid, listnum, changehow)
    elif mode == 5:
        print "Input a Interpret and change a Genre for all matching entries"
        interpretstr = raw_input("Interpret? ")
        interpretlist = interpretstr.split(" ")
        idlist = DB.listbycriteria(interpretlist)
        if idlist == []:
            print "There is no interpret like this. Try again."
        else:
            genre = raw_input('Input genre you want to add: ')
            #changehow = raw_input('How should the genre be added (Options: APPEND, NEW)? ')
            for aid in idlist:
                changehow = "APPEND"
                gflag = True
                for ex_genre in DB.entrys[aid].genre:
                    if ex_genre == genre:
                        gflag = False
                    if ex_genre == "nogenre":
                        changehow = "NEW"
                if gflag:
                    DB.modifyentry("GENRE", genre, aid, None, changehow)
    elif mode == 4:
        entryid = intinput('Input ID of entry to modify multiple times: ')
        spec = ""
        while(spec != "EXIT"):
            spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET, EXIT): ')
            if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
                newspec = raw_input('Input the new value of the choosen spec: ')
                DB.modifyentry(spec, newspec, entryid)
            elif spec == "GENRE" or spec == "INTERPRET":
                changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW, CHANGE)? ')
                if changehow == "APPEND" or changehow == "NEW":
                    newspec = raw_input('Input the new value of the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ","%")
                    DB.modifyentry(spec, newspec, entryid, None, changehow)
                elif changehow == "CHANGE":
                    newspec = raw_input('Input the new value of the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ", "%")
                    listnum = intinput('Input the index you what to change in the speclist: ')
                    DB.modifyentry(spec,newspec, entryid, listnum, changehow)
    elif mode == 2:
        startid = intinput('Input ID of first entry to modify: ')
        endid = intinput('Input ID of last entry to modify: ')
        spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET): ')
        if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
            submode = raw_input('0: Change for all, 1: Ask for every entry ')
            if submode == "0":
                newspec = raw_input('Input the new value of the choosen spec: ')
                for i in range(startid, endid+1):
                    DB.modifyentry(spec, newspec, i)
            if submode == "1":
                for i in range(startid, endid+1):
                    DB.entrys[i].printentry()
                    newspec = raw_input('Input the new value of the choosen spec: ')
                    DB.modifyentry(spec, newspec, i)
            #newspec = raw_input('Input the new value of the choosen spec: ')
            #DB.modifyentry(spec, newspec, startid, endid )
        elif spec == "GENRE" or spec == "INTERPRET":
            submode = intinput('0: Change for all, 1: Ask for every entry ')
            if submode == 0:
                changehow = raw_input('How should the spec be changed (Options: APPEND, NEW, CHANGE)? ')
                if changehow == "APPEND" or changehow == "NEW":
                    newspec = raw_input('Input the new value for the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ", "%")
                    for i in range(startid, endid+1):
                        DB.modifyentry(spec, newspec, i, None, changehow)
                elif changehow == "CHANGE":
                    newspec = raw_input('Input the new value for the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ", "%")
                    listnum = intinput('Input the index you what to change in the speclist: ')
                    for i in range(startid, endid+1):
                        DB.modifyentry(spec,newspec, i, listnum, changehow)
                else:
                    raw_input('Wrong spec reference! Press any key to contionue')
            elif submode == 1:
                subsubmode = intinput('Should the spec always be changes in the same way?0: Yes, 1: No' )
                if subsubmode == 0:
                    changehow = raw_input('How should the spec be changed (Options: APPEND, NEW, CHANGE)? ')
                    if changehow == "APPEND" or changehow == "NEW":
                        for i in range(startid, endid+1):
                            DB.entrys[i].printentry()
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            DB.modifyentry(spec, newspec, i, None, changehow)
                    elif changehow == "CHANGE":
                        listnum = intinput('Input the index you what to change in the speclist: ')
                        for i in range(startid, endid+1):
                            DB.entrys[i].printentry()
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            DB.modifyentry(spec,newspec, startid, listnum, changehow)
                    else:
                        raw_input('Wrong spec reference! Press any key to contionue')
                elif subsubmode == 1:
                    for i in range(startid, endid+1):
                        DB.entrys[i].printentry()
                        changehow = raw_input('How should the spec be changed (Options: APPEND, NEW, CHANGE)? ')
                        if changehow == "APPEND" or changehow == "NEW":
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            DB.modifyentry(spec, newspec, startid, None, changehow)
                        elif changehow == "CHANGE":
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            listnum = intinput('Input the index you what to change in the speclist: ')
                            DB.modifyentry(spec,newspec, startid, listnum, changehow)
                        else:
                            raw_input('Wrong spec reference! Press any key to contionue')
    elif mode == 3:
        print "Input IDs. To stop type -1"
        typedid = 0
        idlist = []
        while(typedid != -1):
            typedid = intinput('Input ID to be modifyed: ')
            if typedid != -1:
                idlist.append(typedid)
        spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET): ')
        if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
            submode = raw_input('0: Change for all, 1: Ask for every entry ')
            if submode == "0":
                newspec = raw_input('Input the new value of the choosen spec: ')
                for ids in idlist:
                    DB.modifyentry(spec, newspec, ids)
            if submode == "1":
                for ids in idlist:
                    DB.entrys[ids].printentry()
                    newspec = raw_input('Input the new value of the choosen spec: ')
                    DB.modifyentry(spec, newspec, ids)
        elif spec == "GENRE" or spec == "INTERPRET":
            submode = raw_input('0: Change for all, 1: Ask for every entry ')
            if submode == "0":
                changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW)? ')
                if changehow == "APPEND" or changehow == "NEW":
                    newspec = raw_input('Input the new value for the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ", "%")
                    for ids in idlist:
                        DB.modifyentry(spec, newspec, ids, None, changehow)
            if submode == "1":
                changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW)? ')
                if changehow == "APPEND" or changehow == "NEW":
                    for ids in idlist:
                        DB.entrys[ids].printentry()
                        newspec = raw_input('Input the new value for the choosen spec: ')
                        if spec == "INTERPRET":
                            newspec = newspec.replace(" ", "%")
                        DB.modifyentry(spec, newspec, ids, None, changehow)
            """
            elif changehow == "CHANGE":
                newspec = raw_input('Input the new value of the choosen spec: ')
                listnum = int(raw_input('Input the index you what to change in the speclist: '))
                DB.modifyentry(spec,newspec, entryid, None, listnum, changehow)
            """
    else:
        raw_input('Invalid Mode. Press key to continue')


def removeentrys(DB):
    print "Seaching for noexisting Files in the Database and searches for new Files in the filesystem."
    DB.removeentrys()
    DB.removeentrys()
    execflag = 1
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            flag = printaentry2(DB,False, None)
        if execflag == 4:
            printbycriteria(DB)
        if execflag == 0:
            return False
        if flag == False:
            break

def statisticsmode(DB):
    print "What Statistic?"
    print "1: Genre, 2: Interpret, 3: Studio, 4: Rating"
    mode = intinput("Choose Mode: ")
    numofentrys = DB.getnumberofentrys()
    os.system("clear")
    print makestring("-",132)
    print makestring("-",55)+" Project Mimir "+backend.getVersion()+" "+makestring("-",55)
    print makestring("-",132)
    print "-"+makestring(" ",5)+"Total number of entrys: "+str(numofentrys)
    print "-"+makestring(" ",130)+"-"
    genrelist = []
    genrenumlist = []
    interpretlist = []
    interpretnumlist = []
    studiolist = []
    studionumlist = []
    ratinglist = []
    ratingnumlist = []
    genre2Dlist = []
    for i in range(0,numofentrys):
        if mode == 1:
            tmpgenre = DB.entrys[i].getSpec("GENRE")
            for genre in tmpgenre:
                flag = True
                jasnum = 0
                for j in genrelist:
                    if j == genre:
                        flag = False
                        rememberindex = jasnum
                    jasnum = jasnum + 1
                if flag == True:
                    genrelist.append(genre)
                    genrenumlist.append(int(1))
                if flag == False:
                    genrenumlist[rememberindex] = genrenumlist[rememberindex] + 1
        if mode == 2:
            tmpinterpret = DB.entrys[i].getSpec("INTERPRET")
            for interpret in tmpinterpret:
                flag = True
                jasnum = 0
                for j in interpretlist:
                    if j == interpret:
                        flag = False
                        rememberindex = jasnum
                    jasnum = jasnum + 1
                if flag == True:
                    interpretlist.append(interpret)
                    interpretnumlist.append(int(1))
                if flag == False:
                    interpretnumlist[rememberindex] = interpretnumlist[rememberindex] + 1
        if mode == 3:
            studio = DB.entrys[i].getSpec("STUDIO")
            flag = True
            jasnum = 0
            for j in studiolist:
                if j == studio:
                    flag = False
                    rememberindex = jasnum
                jasnum = jasnum + 1
            if flag == True:
                studiolist.append(studio)
                studionumlist.append(int(1))
            if flag == False:
                studionumlist[rememberindex] = studionumlist[rememberindex] + 1
        if mode == 4:
            rating = DB.entrys[i].getSpec("RATING")
            flag = True
            jasnum = 0
            for j in ratinglist:
                if j == rating:
                    flag = False
                    rememberindex = jasnum
                jasnum = jasnum + 1
            if flag == True:
                ratinglist.append(rating)
                ratingnumlist.append(int(1))
            if flag == False:
                ratingnumlist[rememberindex] = ratingnumlist[rememberindex] + 1
    if mode == 1:
        for k in range(len(genrelist)):
                genre2Dlist.append([genrelist[k],genrenumlist[k]])
        genre2Dlist = sorted(genre2Dlist, key=itemgetter(1), reverse=True)
        maxlen = 0
        for i in genrelist:
            if len(i) >= maxlen:
                maxlen = len(i)
        for i in range(len(genrelist)):
            emptyspace = maxlen - len(genre2Dlist[i][0])
            print "-"+makestring(" ",5)+genre2Dlist[i][0]+makestring(" ",emptyspace)+" | "+str(genre2Dlist[i][1])
        print "-"+makestring(" ",130)+"-"
        print "-"+makestring(" ",130)+"-"
    if mode == 2:
        maxlen = 0
        for i in interpretlist:
            if len(i) >= maxlen:
                maxlen = len(i)
        for i in range(len(interpretlist)):
            emptyspace = maxlen - len(interpretlist[i])
            print "-"+makestring(" ",5)+interpretlist[i].replace("%"," ")+makestring(" ",emptyspace)+" | "+str(interpretnumlist[i])
        print "-"+makestring(" ",130)+"-"
        print "-"+makestring(" ",130)+"-"
    if mode == 3:
        maxlen = 0
        for i in studiolist:
            if len(i) >= maxlen:
                maxlen = len(i)
        for i in range(len(studiolist)):
            emptyspace = maxlen - len(studiolist[i])
            print "-"+makestring(" ",5)+studiolist[i].replace("%"," ")+makestring(" ",emptyspace)+" | "+str(studionumlist[i])
        print "-"+makestring(" ",130)+"-"
        print "-"+makestring(" ",130)+"-"
    if mode == 4:
        maxlen = 0
        for i in ratinglist:
            if len(i) >= maxlen:
                maxlen = len(i)
        for i in range(len(ratinglist)):
            emptyspace = maxlen - len(ratinglist[i])
            print "-"+makestring(" ",5)+ratinglist[i].replace("%"," ")+makestring(" ",emptyspace)+" | "+str(ratingnumlist[i])
   #print genrelist,genrenumlist
   #print interpretlist, interpretnumlist
   #print studiolist, studionumlist
   #print ratinglist, ratingnumlist
    raw_input('press anything')




def main():
    os.system("resize -s "+str(getheight())+" "+str(getwidth()))
    Code = 999
    DBexists = False
    ignore = False
    criteriaprint = False
    directory = "" #add
    DBexists = False #add
    if len(sys.argv) >= 2:
        print "Hallo"
        directory = sys.argv[1]
        DB = backend.database(1,directory)
        if DB.worked == False:
            raw_input("Please press a key")
            ignore = True
        else:
            DBexists = True
    marked = []
    while(Code != 0):
        os.system("clear")
        banner(directory)
        Code = intinput('Input Code: ')
        if Code == 99:
            if DBexists == True:
                DBexists = DBoptions(DB, DBexists, directory)
            elif DBexists == False:
                inp = raw_input("Is the DB already created? Yes/No")
                if inp == "Yes":
                    directory = raw_input('Input directory where database file is located: ')
                    DB = backend.database(1,directory)
                    if DB.worked == False:
                        raw_input("Please press a key")
                        ignore = True
                    else:
                        DBexists = True
                elif inp =="No":
                    directory = raw_input('Input starting directory:')
                    DB = backend.database(0,directory)
                    DBexists = True
        if DBexists == True:
            if Code == 1:
                execute(DB)
            if Code == 2:
                modifyaentry(DB)
            if Code == 3:
                printaentry2(DB, False, None)
            if Code == 9:
                if criteriaprint == True:
                    executeranlist(DB, idlist)
                else:
                    executeranlist(DB, "all")
            if Code == 5:
                statisticsmode(DB)
            if Code == 4:
                advancedprinting(DB, "")
            if Code == 0:
                print "Exiting!"
                os.system("clear")
        elif Code == 0:
            print "Exiting!"
            os.system("clear")
        else:
            if ignore == False:
                print "Please input valid Code!"
                raw_input('Input anything to go on')




if __name__ == '__main__':
    main()
