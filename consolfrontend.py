#Frontend for usage of Project Mimir in Terminal
import backend
import os

def makestring(symbol, lengths):
    string = ""
    for i in range(0,lengths):
        string = string + symbol
    return string

def banner():
    print makestring("-",132)
    print makestring("-",55)+" Project Mimir v0.1.0 "+makestring("-",55)
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
    print "-"+makestring(" ",5)+"  42 | Help                 | Get a few informations and help                                                                -"
    print "-"+makestring(" ",5)+"  96 | Create new DB        | Create a new Database. From the starting directory, files matching a list of datatypes are     -"
    print "-"+makestring(" ",10)+    " "+makestring(" ",22)+"| added as entrys to the database                                                                -"
    print "-"+makestring(" ",5)+"  97 | Read existing DB     | A previously saved database is loaded                                                          -"
    print "-"+makestring(" ",5)+"  98 | Search for new Files | Search for new Files in a given directory and subirectorys and adds them as entrys             -"
    print "-"+makestring(" ",5)+"  99 | Save DB              | Saves the current database in a File                                                           -"
    print "-"+makestring(" ",130)+"-"
  #  print "-"+makestring(" ",106)+"Created by K. Schweiger -"
    print makestring("-",132)

def execute(DB):
    idtoexecute = int(raw_input('Input ID of entry, to be executer: '))
    DB.runentry(idtoexecute)



def searchnewfiles():
    directory = raw_input('Input directory where database file is located:')
    DB.findnewfiles(directory)



def printaentry(DB):
    print "Printing Mode"
    mode = int(raw_input('Mode? 1: Single entry, 2: Range of entrys '))
    if mode == 1:
        idtoshow = int(raw_input('Input  ID: '))
        DB.entrys[idtoshow].printentry()
        raw_input('Input anything to go on')
    elif mode == 2:
        startid = int(raw_input('Input first ID of range: '))
        endid = int(raw_input('Input last ID of range: '))
        for i in range(startid, endid+1):
            DB.entrys[i].printentry()
        raw_input('Input anything to go on')
    else:
        raw_input('Invalid Mode. Press key to continue')
        


def modifyaentry(DB):
    print "Modifying Mode"
    mode = int(raw_input('Mode? 1: Single entry, 2: Range of entrys '))
    if mode == 1:
        entryid = int(raw_input('Input ID of entry to modify: '))
        spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET): ')
        if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
            newspec = raw_input('Input the new value of the choosen spec: ')
            DB.modifyentry(spec, newspec, entryid)
        elif spec == "GENRE" or spec == "INTERPRET":
            changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW, CHANGE)? ')
            if changehow == "APPEND" or changehow == "NEW":
                newspec = raw_input('Input the new value of the choosen spec: ')
                DB.modifyentry(spec, newspec, entryid, None, None, changehow)
            elif changehow == "CHANGE":
                newspec = raw_input('Input the new value of the choosen spec: ')
                listnum = int(raw_input('Input the index you what to change in the speclist: '))
                DB.modifyentry(spec,newspec, entryid, None, listnum, changehow)
    elif mode == 2:
        startid = int(raw_input('Input ID of first entry to modify: '))
        endid = int(raw_input('Input ID of last entry to modify: '))
        spec = raw_input('Input spec you whant to modify (Options: NAME, STUDIO, RATING,GENRE,INTERPRET): ')
        if spec == "NAME" or spec == "STUDIO" or spec == "RATING":
            newspec = raw_input('Input the new value of the choosen spec: ')
            DB.modifyentry(spec, newspec, startid, endid )
        elif spec == "GENRE" or spec == "INTERPRET":
            changehow = raw_input('How should the Spec be changed (Options: APPEND, NEW, CHANGE)? ')
            if changehow == "APPEND" or changehow == "NEW":
                newspec = raw_input('Input the new value of the choosen spec: ')
                DB.modifyentry(spec, newspec, startid, endid, None, changehow)
            elif changehow == "CHANGE":
                newspec = raw_input('Input the new value of the choosen spec: ')
                listnum = int(raw_input('Input the index you what to change in the speclist: '))
                DB.modifyentry(spec,newspec, startid, endid, listnum, changehow)
    else:
        raw_input('Invalid Mode. Press key to continue')



def printbycriteria(DB):
    print "Print by Criteria"
    criterianum = int(raw_input('Input the number of criteria: '))
    criterialist = []
    for i in range(0,criterianum):
        print i+1,"of",criterianum
        criteria = raw_input('Input criteria: ')
        criterialist.append(criteria)
    DB.printbycriteria(criterialist)
    raw_input('Input anything to go on')



def main():
    os.system("resize -s 43 132")
    Code = 999
    DBexists = False
    while(Code != 0):
        os.system("clear")
        banner()
        Code = int(raw_input('Input Code: '))
        if Code == 96:
            if DBexists == False:
                directory = raw_input('Input starting directory:')
                DB = backend.database(0,directory)
                DBexists = True
            else:
                print "There is already a Database" 
                raw_input('Input anything to go on')
        elif Code == 97:
            if DBexists == False:
                directory = raw_input('Input directory where database file is located: ')
                DB = backend.database(1,directory)
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
            if Code == 98:
                searchnewfiles()
            if Code == 99:
                DB.saveDB()
            if Code == 0:
                print "Exiting!"
                os.system("clear")   
        elif Code == 0:
            print "Exiting!"
            os.system("clear")
        else:
            print "Please input valid Code!"
            raw_input('Input anything to go on')




if __name__ == '__main__':
    main()