#Frontend for usage of Project Mimir in Terminal
# MTF (MimirTerminalFrontend) v0.2.5 
#2014, K. Schweiger
import backend
import os
import random

def makestring(symbol, lengths):
    string = ""
    for i in range(0,lengths):
        string = string + symbol
    return string

def banner(database):
    print makestring("-",132)
    print makestring("-",55)+" Project Mimir "+backend.getVersion()+" "+makestring("-",55)
    print makestring("-",132)
    print "-"+makestring(" ",130)+"-"
    print "-"+makestring(" ",5)+"Code | Name                 | Comments                                                                                       -"
    print "-"+makestring(" ",5)+"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    -"
    print "-"+makestring(" ",5)+"   0 | Exit                 |                                                                                                -"
    print "-"+makestring(" ",5)+"   1 | Execute              | Opens the selected Entry in an external Applicatiom                                            -"
    print "-"+makestring(" ",5)+"   2 | Modify               | Modify Name, Genres, Interprets, Studio and Rating. Genres and Interprets are Lists, so you    -"
    print "-"+makestring(" ",10)+    " "+makestring(" ",22)+"| can Append and Modify Elements or overwrite the list                                           -"
    print "-"+makestring(" ",5)+"   3 | Print Information    | Prints the informations of a given entry (Input: ID)                                           -"
    print "-"+makestring(" ",5)+"   4 | Random !!!!          | Execute a Random Entry. If printed by criteria, execute one of these                           -"
    print "-"+makestring(" ",5)+"   5 | Statistics           | Choose between different statistics                                                            -"
    print "-"+makestring(" ",5)+"  42 | Help                 | Get a few informations and help                                                                -"
    print "-"+makestring(" ",5)+"  99 | DB options           | Options for modifieing the DB                                                                  -"
    print "-"+makestring(" ",130)+"-"
    print "- "+str(database)+makestring(" ",118-len(database))+"MTF v0.2.5 -"
    print makestring("-",132)

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

def DBoptions(DB, DBexists):
    print "+---+-------Options--------+"
    #print "| 0 | Exit                 |"
    print "| 1 | Create new DB        |"
    print "| 2 | Read existing DB     |"
    print "| 3 | Remove Entrys        |"
    print "| 4 | Search for new Files |"
    print "| 5 | Save DB              |"
    print "+---+----------------------+"
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
            searchnewfiles(DB)
        else:
            print "There is no DB yet"
    elif Code == 5:
        if DBexists == True:
            DB.saveDB()
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
            tmplen = len(spec)
        #look if the spec is the longest
        if tmplen > maxSpeclen:
            maxSpeclen = tmplen
            maxlenid = i
            maxSinglelen = tmpSinglelen
    maxlenlist = [maxSpeclen]
    maxlenlist = maxlenlist + maxSinglelen
    return  maxlenlist
    


def execute(DB):
    idtoexecute = int(raw_input('Input ID of entry, to be executed: '))
    if idtoexecute == -1:
       idtoexecute = random.randint(0, DB.getnumberofentrys())
    print "Now playing:",DB.entrys[idtoexecute].getSpec("NAME")
    DB.runentry(idtoexecute)
    
def executeranlist(DB, idlist):
    if idlist == "all":
        idtoexecute = random.randint(0, DB.getnumberofentrys())
        print "Now playing:",DB.entrys[idtoexecute].getSpec("NAME")
        DB.runentry(idtoexecute)
    else:
        listentry = random.randint(0, len(idlist))
        print "Now playing:",DB.entrys[idlist[listentry]].getSpec("NAME")
        DB.runentry(idlist[listentry])
    

def searchnewfiles(DB):
    directory = raw_input('Input directory where database file is located:')
    DB.findnewfiles(directory)



def printaentry(DB):
    print "Printing Mode"
    mode = intinput('Mode? 1: Single entry, 2: Range of entrys ')
    if mode == 1:
        idtoshow = int(raw_input('Input  ID: '))
        DB.entrys[idtoshow].printentry(None)
        #raw_input('Input anything to go on')
    elif mode == 2:
        startid = int(raw_input('Input first ID of range: '))
        endid = int(raw_input('Input last ID of range: '))
        SpecstoPrint = ["GENRE","INTERPRET","STUDIO"]
        lengths = []
        for spec in SpecstoPrint:
            lengths.append(findmaxSpeclen(DB,startid,endid,spec))
        #print lengths
        header =  "ID"+makestring(" ",2)+"NAME"+makestring(" ",18)
        subheader = makestring("-",3)+makestring(" ",1)+makestring("-",21)+makestring(" ",1)
        for i in range(len(lengths)):
            if lengths[i][0] != 0:
                header = header+SpecstoPrint[i]+makestring(" ",lengths[i][0]-len(SpecstoPrint[i]))+" "
                subheader = subheader + makestring("-",lengths[i][0])+makestring(" ",1)
        print header
        print subheader
        for i in range(startid, endid+1):
            DB.entrys[i].printentry(lengths)
        #raw_input('Input anything to go on')
    else:
        raw_input('Invalid Mode. Press key to continue')
    execflag = 1
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            flag = printaentry2(DB)
        if execflag == 4:
            if criteriaprint == True:
                executeranlist(DB, idlist)
            else:
                executeranlist(DB, "all")
        if execflag == 0:
            return False
        if flag == False:
            break


def printaentry2(DB):
    print "Printing Mode"
    jump = False
    criteriaprint = False
    print "+---+-------------------+"
    print "| 1 | Single entry      |"
    print "| 2 | Range of entrys   |"
    print "| 3 | Print by criteria |"
    print "| 4 | Print all         |"
    print "+---+-------------------+"
    mode = intinput('Choose Mode: ')
    if mode == 1:
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
        criterianum = intinput('Input the number of criteria: ')
        criterialist = []
        for i in range(0,criterianum):
            print i+1,"of",criterianum
            criteria = raw_input('Input criteria: ')
            criterialist.append(criteria)
        idlist =  DB.listbycriteria(criterialist)
        jump = True
        criteriaprint = True
    elif mode == 4:
        idlist =  DB.listbycriteria([])
        jump = True
    else:
        jump = False
    #Code for nice printing
    if jump == True:
        SpecstoPrint = ["GENRE","INTERPRET","STUDIO"]
        lengths = []
        for spec in SpecstoPrint:
            lengths.append(findmaxSpeclen(DB,idlist,spec))
        if lengths[0][0] <= 5:
            lengths[0][0] = 5
        if lengths[1][0] <= 9:
            lengths[1][0] = 9
        if lengths[2][0] <= 6:
            lengths[2][0] = 6
        #print lengths
        header =  "ID"+makestring(" ",3)+"NAME"+makestring(" ",18)
        subheader = makestring("-",3)+makestring(" ",2)+makestring("-",21)+makestring(" ",1)
        for i in range(len(lengths)):
            if lengths[i][0] != 0:
                header = header+SpecstoPrint[i]+makestring(" ",lengths[i][0]-len(SpecstoPrint[i]))+" "
                subheader = subheader + makestring("-",lengths[i][0])+makestring(" ",1)
        print header
        print subheader
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
            if lengths == None:
                printedstring = idprint+"  "+nameprint+"  "
                if genreflag == True:
                    printedstring = printedstring+" "+' '.join(genreprint)
                if interpretflag == True:
                    printedstring = printedstring+" "+(' '.join(interpretprint)).replace("%"," ")
                if studioflag == True:
                    printedstring = printedstring+" "+studioprint
            else:
                printedstring = idprint+"  "+nameprint
                printedgenre = ""
                printedinterpret = ""
                printedstudio = ""
                if genreflag == True:
                    i = -1
                    glen = 0
                    for g in genreprint:
                        printedgenre = printedgenre + " "  + g
                        glen = glen + len(g)
                        i = i + 1
                    glen = glen + i
                    #print glen, i
                    if glen < lengths[0][0]:
                        printedgenre = printedgenre + makestring(" ",lengths[0][0]-glen)
                if genreflag == False:
                    printedgenre = " " +  makestring(" ",lengths[0][0])
                printedstring = printedstring + printedgenre
                if interpretflag == True:
                    i = -1
                    ilen = 0
                    for inter in interpretprint:
                        printedinterpret = printedinterpret + " " + inter.replace("%"," ")
                        ilen = ilen + len(inter)
                        i = i + 1
                    ilen = ilen + i
                    if ilen < lengths[1][0]:
                        printedinterpret = printedinterpret + makestring(" ",lengths[1][0]-ilen)
                if interpretflag == False:
                    printedinterpret = " " + makestring(" ",lengths[1][0])
                printedstring = printedstring + printedinterpret
                if studioflag == True:
                    printedstudio = " " + studioprint + makestring(" ",lengths[2][0]-len(studioprint))
                if studioflag == False:
                    printedstudio = " " + makestring(" ",lengths[2][0])
                printedstring = printedstring + printedstudio
            print printedstring            
        #raw_input('Input anything to go on')
    else:
        raw_input('Invalid Mode. Press key to continue')
    execflag = 1
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            flag = printaentry2(DB)
        if execflag == 4:
            if criteriaprint == True:
                executeranlist(DB, idlist)
            else:
                executeranlist(DB, "all")
        if execflag == 0:
            return False
        if flag == False:
            break




def modifyaentry(DB):
    print "Modifying Mode"
    mode = intinput('Mode? (1: Single entry, 2: Range of entrys, 3: List of entrys) ')
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
                        DB.modifyentry(spec, newspec, ids, None, None, changehow)
            if submode == "1":
                changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW)? ')
                if changehow == "APPEND" or changehow == "NEW":
                    for ids in idlist:
                        DB.entrys[ids].printentry()
                        newspec = raw_input('Input the new value for the choosen spec: ')
                        if spec == "INTERPRET":
                            newspec = newspec.replace(" ", "%")
                        DB.modifyentry(spec, newspec, ids, None, None, changehow)
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
            flag = printaentry2(DB)
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
        maxlen = 0
        for i in genrelist:
            if len(i) >= maxlen:
                maxlen = len(i)
        for i in range(len(genrelist)):
            emptyspace = maxlen - len(genrelist[i])
            print "-"+makestring(" ",5)+genrelist[i]+makestring(" ",emptyspace)+" | "+str(genrenumlist[i])
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
    os.system("resize -s 43 132")
    Code = 999
    DBexists = False
    ignore = False
    criteriaprint = False
    directory = ""

    DBexists = True
    while(Code != 0):
        os.system("clear")
        banner(directory)
        Code = intinput('Input Code: ')
        if Code == 99:
            DBexists = DBoptions(DB, DBexists)
        """
        if Code == 95:
            if DBexists == False:
                directory = raw_input('Input starting directory:')
                DB = backend.database(0,directory)
                DBexists = True
            else:
                print "There is already a Database" 
                raw_input('Input anything to go on')
        elif Code == 96:
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
        """
        if DBexists == True:
            if Code == 1:
                execute(DB)
            if Code == 2:
                modifyaentry(DB)
            if Code == 3:
                printaentry2(DB)
            if Code == 4:
                if criteriaprint == True:
                    executeranlist(DB, idlist)
                else:
                    executeranlist(DB, "all")
            if Code == 5:
                statisticsmode(DB)
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
