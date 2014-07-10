#Frontend for usage of Project Mimir in Terminal
# MTF (MimirTerminalFrontend) v0.1.2 
#2014, K. Schweiger
import backend
import os

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
    print "-"+makestring(" ",5)+"   4 | Print by Criteria    | Input a list of criterias and all matching entrys are printed                                  -"
    print "-"+makestring(" ",5)+"   5 | Statistics           | Choose between different statistics                                                            -"
    print "-"+makestring(" ",5)+"  42 | Help                 | Get a few informations and help                                                                -"
    print "-"+makestring(" ",5)+"  95 | Create new DB        | Create a new Database. From the starting directory, files matching a list of datatypes are     -"
    print "-"+makestring(" ",10)+    " "+makestring(" ",22)+"| added as entrys to the database                                                                -"
    print "-"+makestring(" ",5)+"  96 | Read existing DB     | A previously saved database is loaded                                                          -"
    print "-"+makestring(" ",5)+"  97 | Remove Entrys        | Search for new nonexisting Files in the database and removes them. Also adds new files         -"
    print "-"+makestring(" ",5)+"  98 | Search for new Files | Search for new Files in a given directory and subirectorys and adds them as entrys             -"
    print "-"+makestring(" ",5)+"  99 | Save DB              | Saves the current database in a File                                                           -"
    print "-"+makestring(" ",130)+"-"
    print "- "+str(database)+makestring(" ",118-len(database))+"MTF v0.1.4 -"
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



def execute(DB):
    idtoexecute = int(raw_input('Input ID of entry, to be executer: '))
    DB.runentry(idtoexecute)
    


def searchnewfiles(DB):
    directory = raw_input('Input directory where database file is located:')
    DB.findnewfiles(directory)



def printaentry(DB):
    print "Printing Mode"
    mode = intinput('Mode? 1: Single entry, 2: Range of entrys ')
    if mode == 1:
        idtoshow = int(raw_input('Input  ID: '))
        DB.entrys[idtoshow].printentry()
        #raw_input('Input anything to go on')
    elif mode == 2:
        startid = int(raw_input('Input first ID of range: '))
        endid = int(raw_input('Input last ID of range: '))
        for i in range(startid, endid+1):
            DB.entrys[i].printentry()
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
            flag = printaentry(DB)
        if execflag == 4:
            printbycriteria(DB)
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
                DB.modifyentry(spec, newspec, entryid, None, None, changehow)
            elif changehow == "CHANGE":
                newspec = raw_input('Input the new value of the choosen spec: ')
                if spec == "INTERPRET":
                    newspec = newspec.replace(" ", "%")
                listnum = intinput('Input the index you what to change in the speclist: ')
                DB.modifyentry(spec,newspec, entryid, None, listnum, changehow)
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
                        DB.modifyentry(spec, newspec, i, None, None, changehow)
                elif changehow == "CHANGE":
                    newspec = raw_input('Input the new value for the choosen spec: ')
                    if spec == "INTERPRET":
                        newspec = newspec.replace(" ", "%")
                    listnum = intinput('Input the index you what to change in the speclist: ')
                    for i in range(startid, endid+1):
                        DB.modifyentry(spec,newspec, i, None, listnum, changehow)
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
                            DB.modifyentry(spec, newspec, i, None, None, changehow)
                    elif changehow == "CHANGE":
                        listnum = intinput('Input the index you what to change in the speclist: ')
                        for i in range(startid, endid+1):
                            DB.entrys[i].printentry()
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            DB.modifyentry(spec,newspec, startid, endid, listnum, changehow)
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
                            DB.modifyentry(spec, newspec, startid, endid, None, changehow)
                        elif changehow == "CHANGE":
                            newspec = raw_input('Input the new value for the choosen spec: ')
                            if spec == "INTERPRET":
                                newspec = newspec.replace(" ", "%")
                            listnum = intinput('Input the index you what to change in the speclist: ')
                            DB.modifyentry(spec,newspec, startid, endid, listnum, changehow)
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



def printbycriteria(DB):
    print "Print by Criteria"
    criterianum = intinput('Input the number of criteria: ')
    criterialist = []
    for i in range(0,criterianum):
        print i+1,"of",criterianum
        criteria = raw_input('Input criteria: ')
        criterialist.append(criteria)
    DB.printbycriteria(criterialist)
    execflag = 1
    flag = True
    while(execflag != 0):
        execflag = intinput('Input Code (0 to go to mainmenu): ')
        if execflag == 1:
            execute(DB)
        if execflag == 2:
            modifyaentry(DB)
        if execflag == 3:
            flag = printaentry(DB)
        if execflag == 4:
            printbycriteria(DB)
        if execflag == 0:
            return False
        if flag == False:
            break

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
            flag = printaentry(DB)
        if execflag == 4:
            printbycriteria(DB)
        if execflag == 0:
            return False
        if flag == False:
            break

def statisticsmode(DB):
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
    maxlen = 0
    for i in genrelist:
        if len(i) >= maxlen:
            maxlen = len(i)
    for i in range(len(genrelist)):
        emptyspace = maxlen - len(genrelist[i])
        print "-"+makestring(" ",5)+genrelist[i]+makestring(" ",emptyspace)+" | "+str(genrenumlist[i])
    print "-"+makestring(" ",130)+"-"
    print "-"+makestring(" ",130)+"-"
    maxlen = 0
    for i in interpretlist:
        if len(i) >= maxlen:
            maxlen = len(i)
    for i in range(len(interpretlist)):
        emptyspace = maxlen - len(interpretlist[i])
        print "-"+makestring(" ",5)+interpretlist[i].replace("%"," ")+makestring(" ",emptyspace)+" | "+str(interpretnumlist[i])
    print "-"+makestring(" ",130)+"-"
    print "-"+makestring(" ",130)+"-"
    maxlen = 0
    for i in studiolist:
        if len(i) >= maxlen:
            maxlen = len(i)
    for i in range(len(studiolist)):
        emptyspace = maxlen - len(studiolist[i])
        print "-"+makestring(" ",5)+studiolist[i].replace("%"," ")+makestring(" ",emptyspace)+" | "+str(studionumlist[i])
    print "-"+makestring(" ",130)+"-"
    print "-"+makestring(" ",130)+"-"
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
    directory = ""
    while(Code != 0):
        os.system("clear")
        banner(directory)
        Code = intinput('Input Code: ')
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
        if DBexists == True:
            if Code == 1:
                execute(DB)
            if Code == 2:
                modifyaentry(DB)
            if Code == 3:
                printaentry(DB)
            if Code == 4:
                printbycriteria(DB)
            if Code == 5:
                statisticsmode(DB)
            if Code == 97:
                removeentrys(DB)
            if Code == 98:
                searchnewfiles(DB)
            if Code == 99:
                DB.saveDB()
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
