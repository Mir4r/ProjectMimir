#!/usr/bin/env python
#2014-2015, K. Schweiger


import sys
import os
from glob import glob
import time
import missingspecs
import colorprinting

def getVersion():
    return "v0.4.1"

def getcurrentspecs():
    return ["GENRE","INTERPRET","STUDIO","RATED","OPENED","ADDED","NUMOPENED","LASTMOD"]

def gettime(flag):
    lt = time.localtime()
    if flag == "date":
        if int(lt[2]) <= 9:
            if int(lt[1])<= 9:
                   dateres = "0"+str(lt[2])+".0"+str(lt[1])+"."+str(lt[0]-2000)
            else:
                   dateres = "0"+str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        else:
            if int(lt[1]) <= 9:
                   dateres = str(lt[2])+".0"+str(lt[1])+"."+str(lt[0]-2000)
            else:
                   dateres = str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        return dateres
    elif flag == "time":
        timeres = str(lt[3])+":"+str(lt[4])+":"+str(lt[5])
        return timeres
    elif flag == "datetime":
        res = gettime("date")+"|"+gettime("time")
        return res

def makestring(symbol, lengths):
    string = ""
    for i in range(0,lengths):
        string = string + symbol
    return string

class database:
    def __init__(self,flag,startdir):
        #lt = time.localtime()
        #date = str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        self.entrys = []
        self.openids = False
        self.rootdir = startdir
        if flag == 0:
            print "A new DataBase will be created"
            #methode zum einlesen aller datein im Ordner aufrufen
            self.dirs = self.dirfinder(startdir)
            #filelist contains the paths to the files
            self.filelist = []
            for d in self.dirs:
                self.filelist = self.filelist + self.getfiles(d)
            #print self.filelist
            self.id = 0
            for foundfiles in self.filelist:
                # os.path.splitext(os.path.basename(foundfiles))[0] returns the filename without extention
                self.entrys.append(entry(None, self.id, os.path.splitext(os.path.basename(foundfiles))[0], foundfiles, "nogenre","nointerpret","nostudio","notrated","neveropened",gettime("datetime"),0,"nevermod"))
                self.id = self.id + 1
        if flag == 1:
            self.worked = True
            self.dirs = [startdir]
            self.DBlines = self.readDB(startdir)
            if self.DBlines != False:
                for lines in self.DBlines:
                    self.specs = []
                    self.specs = lines.split(" ")
                    self.entrys.append(entry(self.specs))
            else:
               self.worked = False
    #Method for finding all Directorys in the given Directory
    #in the end you get a list with als subdirectorys and the starting directory
    def dirfinder(self, directory):
        self.dirs = [directory]
        #look what is in the givem directory
        for item in glob(os.path.join(directory, '*')):
            #if you find a directory call this method recursive
            if os.path.isdir(item):
                self.dirs = self.dirs + self.dirfinder(item)
        return self.dirs
    #find all .txt files in the given directory and write them in a List
    def getfiles(self, directory):
        self.files = []
        #self.datatypes =  ['*.txt', '*.dat']
        self.datatypes =  ['*.mp4', '*.wmv','*.avi','*.mov','*.mpg','*.mp7','*.flv','*.mkv','*.f4v','*.mpeg']
        for types in self.datatypes:
            for f in glob(os.path.join(directory, types)):
            #self.files.append(os.path.splitext(os.path.basename(f))[0])
                self.files.append(f)
        return sorted(self.files)
    def removeentrys(self):
        removelist = []
        self.lastid = len(self.entrys)
        for i in range(self.lastid):
                try :
                    open(self.entrys[i].getSpec("PATH"))
                except IOError:
                    removelist.append(self.entrys[i].getSpec("ID"))
        #print removelist
        self.tmp = 0
        for j in removelist:
            del self.entrys[int(j)-self.tmp]
            self.tmp = self.tmp + 1
        #for i in range(len(self.entrys)):
        #    self.entrys[i].printentry()
        addedids = []
        filespecs = []
        self.newfile = self.findnewfiles(self.rootdir, addedids,filespecs)
        if self.newfile == False:
            #print "move"
            for j in range(len(self.entrys)):
                if j != int(self.entrys[j].getSpec("ID")):
                    #print "moved", j
                    self.entrys[-1].changeSpec("ID", j)
                    self.entrys.insert(j, self.entrys[-1])
                    del self.entrys[-1]
        return [addedids,filespecs]
    def changedpaths(self, startdir):
        changedlistid = []
        changedlistpath = []
        self.lastid = len(self.entrys)
        for i in range(self.lastid):
                try :
                    open(self.entrys[i].getSpec("PATH"))
                except IOError:
                    changedlistid.append(self.entrys[i].getSpec("ID"))
                    changedlistpath.append(self.entrys[i].getSpec("PATH"))
        self.dirs = self.dirfinder(startdir)
        #filelist contains the paths to the files
        self.filelist = []
        for d in self.dirs:
            self.filelist = self.filelist + self.getfiles(d)
        returnlist = []
        for j in range(len(changedlistid)):
            self.name = os.path.basename(changedlistpath[j]) #Filename of files, that have changed location
            for i in range(len(self.filelist)):
                if os.path.basename(self.filelist[i]) == self.name:
                    self.entrys[int(changedlistid[j])].changeSpec("PATH",self.filelist[i])
                    #print changedlistid[j]," was at ", colorprinting.red(changedlistpath[j]), colorprinting.blue(" and is now at "),colorprinting.green(self.filelist[i])
                    returnlist.append([changedlistid[j],changedlistpath[j],self.filelist[i]])
        return returnlist
    #Read the Database file and returns a list of the lines in the file
    def readDB(self, directory):
        print "ReadDB"
        #open file
        charset = sys.getfilesystemencoding()
        self.lines = []
        subfolder = ".mimir/"
        #read file "main.db" in the starting directory (dirs[0])
        try:
            open(os.path.join(directory+subfolder, 'main.db'), 'r')
        except IOError:
            print "The Database does not exist"
            return False
        with open(os.path.join(directory+subfolder, 'main.db'), 'r') as f:
            self.input = f.read()
        #after this you have one sting with all lines seperatet by \n
        #so split it! -> self.lines is a list with the lines from the read file
        self.lines = self.input.split("\n")
        self.lines.pop()
        return self.lines
    def addentry(self, name, path, genre, interpret, studio,rating):
        print "A new Entry will be added to the DB"
        self.id = len(self.entrys)
        self.entrys.append(entry(None,self.id,name,path,genre,interpret,studio,rating,opened,added,numopened,lastmod))

    def modifyentry(self, changewhat, change, startid, changeindex = None, changehow = None):
        self.index = startid
        if changeindex is None and changehow is None:
            self.entrys[self.index].changeSpec(changewhat,change)
            self.entrys[self.index].changeSpec("LASTMOD",gettime("datetime"))
            #print self.entrys[0].name
        else:
            self.status = self.entrys[self.index].changeSpec(changewhat,change,changehow,changeindex)
            self.entrys[self.index].changeSpec("LASTMOD",gettime("datetime"))
            if self.status == False:
                print "Something went wrong for your modifing request of entry ",self.index
    #Method for saving the filelist
    def saveDB(self):
        subfolder = ".mimir/"
        self.secondaryDB()
        charset = sys.getfilesystemencoding()
        #write a file "fileslist" in the starting directory (dirs[0])
        with open(os.path.join(self.dirs[0].decode(charset)+subfolder, 'main.db'), 'w+') as f:
            for e in self.entrys:
                write_items = f.write(''.join(e.listofelements()))
                write_items = f.write("\n")
    #How does it work?
    #Function gets a list of criteria and looks through all entrys. For each entrys a loop over all criteria begins and looks through the entrys Genres, Interprets and Studios.
    def listbycriteria(self, criterialist):
        self.printlist = []
        for i in range(len(self.entrys)):
            self.toprint = []
            self.printflag = False
            for criteria in criterialist:
                #New Code
                self.negflag = False
                if criteria[0] == "!":
                    self.negflag = True
                    criteria = criteria[1::]
                ###
                self.flag = False
                for genres in self.entrys[i].getSpec("GENRE"):
                    if genres == criteria:
                        self.flag = True
                for interprets in self.entrys[i].getSpec("INTERPRET"):
                    self.names = interprets.split("%")
                    for name in self.names:
                        if name == criteria:
                            self.flag = True
                if self.entrys[i].getSpec("STUDIO") == criteria:
                    self.flag = True
                #New Code
                #print "-----",criteria
                if self.flag == True and self.negflag == True:
                    self.flag = False
                    #print "entryid = ",i
                elif self.flag == False and self.negflag == True:
                    self.flag = True
                    #print "entryid = ",i
                ###
                self.toprint.append(self.flag)
            #print self.toprint
            #print self.toprint
            self.printflag = True
            for j in range(len(self.toprint)):
                if self.toprint[j] == False:
                    self.printflag = False
            if self.printflag == True:
                #self.entrys[i].printentry()
                self.printlist.append(i)
        return self.printlist
    def getbytimesopened(self, nOpened):
        self.printlist = []
        for i in range(len(self.entrys)):
            if self.entrys[i].getSpec("NUMOPENED") == nOpened:
                self.printlist.append(i)
        return self.printlist


    def findnewfiles(self, startdir, ids, foundspecs):
        self.dirs = self.dirfinder(startdir)
        self.insertedflag = False
        #filelist contains the paths to the files
        self.filelist = []
        for d in self.dirs:
            self.filelist = self.filelist + self.getfiles(d)
        #print self.filelist
        print " "
        for foundfile in self.filelist:
            self.existflag = False
            for i in range(len(self.entrys)):
                #print len(self.entrys)
                #print self.entrys[i].getSpec("PATH")
                if self.entrys[i].getSpec("PATH") == foundfile:
                    #print self.entrys[i].getSpec("NAME")
                    self.existflag = True
            if self.existflag == False:
                print "foundfile",foundfile
                self.insertedflag = False
                for i in range(len(self.entrys)):
                    if i != int(self.entrys[i].getSpec("ID")):
                        print "Inserted with ID:",i
                        self.entrys.insert(i, entry(None,i,os.path.splitext(os.path.basename(foundfile))[0], foundfile, "nogenre","nointerpret","nostudio","notrated","neveropened",gettime("datetime"),str(0),"nevermod"))
                        self.insertedflag = True
                        #print os.path.splitext(foundfile)
                        #foundspecs.append(self.findspecsbyfilename(os.path.splitext(os.path.basename(foundfile))[0], startdir))
                        foundspecs.append(self.findspecsbyfilename(os.path.splitext(foundfile)[0], startdir))
                        ids.append(i)
                        break
                if self.insertedflag == False:
                    self.id = len(self.entrys)
                    self.entrys.append(entry(None,self.id,os.path.splitext(os.path.basename(foundfile))[0], foundfile, "nogenre","nointerpret","nostudio","notrated","neveropened",gettime("datetime"),str(0),"nevermod"))
                    self.insertedflag = False
                    #foundspecs.append(self.findspecsbyfilename(os.path.splitext(os.path.basename(foundfile))[0], startdir))
                    foundspecs.append(self.findspecsbyfilename(os.path.splitext(foundfile)[0], startdir))
                    ids.append(self.id)
                    print "Appended with ID:",self.id
#                return self.insertedflag
        return self.insertedflag
    def runentry(self, entryid):
        os.system("vlc -q --one-instance "+str(self.entrys[entryid].getSpec("PATH"))+" 2> /dev/null &")
    def getnumberofentrys(self):
        return len(self.entrys)
    def sortentrys(self):
        self.pathlist = []
        self.tmpentrys = []
        for i in range(len(self.entrys)):
            self.pathlist.append(self.entrys[i].getSpec("PATH"))
        self.pathlist.sort()
        for i in range(len(self.entrys)):
            for j in range(len(self.entrys)):
                if self.entrys[j].getSpec("PATH") == self.pathlist[i]:
                    self.tmpentrys.append(self.entrys[j])
                    break
        if len(self.tmpentrys) != len(self.entrys):
            print "Error! Lists do not match"
            exit()
        self.entrys = self.tmpentrys
    def entryopened(self, idopened):
        #lt = time.localtime()
        #date = str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        self.entrys[idopened].changeSpec("OPENED",gettime("datetime"))
        self.entrys[idopened].changeSpec("NUMOPENED",None)
    def secondaryDB(self):
        subfolder = ".mimir/"
        self.interpretlist = []
        self.genrelist = []
        self.studiolist = []
        for i in range(len(self.entrys)):
            self.tmpinterpret = self.entrys[i].getSpec("INTERPRET")
            for interpret in self.tmpinterpret:
                if interpret not in self.interpretlist:
                    self.interpretlist.append(interpret)
        for i in range(len(self.entrys)):
            self.tmpgenre = self.entrys[i].getSpec("GENRE")
            for genre in self.tmpgenre:
                if genre not in self.genrelist:
                    self.genrelist.append(genre)
        for i in range(len(self.entrys)):
            studio = self.entrys[i].getSpec("STUDIO")
            if studio not in self.studiolist:
                self.studiolist.append(studio)
        #print self.interpretlist
        #print self.genrelist
        #print self.studiolist
        charset = sys.getfilesystemencoding()
        #write a file "fileslist" in the starting directory (dirs[0])
        with open(os.path.join(self.dirs[0].decode(charset)+subfolder, 'genres.db'), 'w+') as f:
            for g in self.genrelist:
                write_items = f.write(g)
                write_items = f.write("\n")
        with open(os.path.join(self.dirs[0].decode(charset)+subfolder, 'interprets.db'), 'w+') as f:
            for g in self.interpretlist:
                write_items = f.write(g.replace("%"," "))
                write_items = f.write("\n")
        with open(os.path.join(self.dirs[0].decode(charset)+subfolder, 'studios.db'), 'w+') as f:
            for g in self.studiolist:
                write_items = f.write(g)
                write_items = f.write("\n")
    def readsecondaryDB(self, directory):
        charset = sys.getfilesystemencoding
        DBs = ["genres.db","interprets.db","studios.db"]
        secondaryDBs = []
        subfolder = ".mimir/"
        for i in range(3):
            self.lines = []
            #read file "main.db" in the starting directory (dirs[0])
            try:
                open(os.path.join(directory+subfolder, DBs[i]), 'r')
            except IOError:
                print "The secondaryDBs are not created yet"
                return False
            with open(os.path.join(directory+subfolder, DBs[i]), 'r') as f:
                self.input = f.read()
            #after this you have one sting with all lines seperatet by \n
            #so split it! -> self.lines is a list with the lines from the read file
            self.lines = self.input.split("\n")
            self.lines.pop()
            secondaryDBs.append(self.lines)
        return secondaryDBs
    def findspecsbyfilename(self, filename, directory):
        secondaryDBs = self.readsecondaryDB(directory)
        candidates = []
        #fist seperate the filename in smaller strings, that could have a meaning
        commonseparators = [",",".","_","-","/"]
        for seperator in commonseparators:
            filename = filename.replace(seperator," ")
        filename = filename.lower()
        parts = filename.split(" ") #contains the smaller strings
        #print parts
        for DB in secondaryDBs:
            tmp = []
            for element in DB:
                if (element.replace(" ","")).lower() in parts:
                    tmp.append(element)
                for elem in element.split(" "):
                    if elem.lower() in parts:
                        tmp.append(element)
            candidates.append(tmp)
        return candidates

class entry():
    def __init__(self, specs, ID=None, name=None, path=None, genre=None, interpret=None, studio=None, rating=None, opened=None, added=None, numopened=None, lastmod =None):
        if specs is None:
            self.genre = []
            self.interpret = []
            self.id=ID
            self.name=name
            self.path=path
            self.genre.append(genre)
            self.interpret.append(interpret)
            self.studio=studio
            self.rating=rating
            self.opened=opened
            self.added=added
            self.numopened=numopened
            self.lastmod=lastmod
        else:
            self.genre = []
            self.interpret = []
            for num in specs:
                self.spec = num.split('$')
                if self.spec[0] == "ID":
                    self.id = self.spec[1]
                if self.spec[0] == "NAME":
                    self.name = self.spec[1]
                if self.spec[0] == "PATH":
                    self.path = self.spec[1]
                if self.spec[0] == "GENRE":
                    self.genre.append(self.spec[1])
                if self.spec[0] == "INTERPRET":
                    self.interpret.append(self.spec[1])
                if self.spec[0] == "STUDIO":
                    self.studio = self.spec[1]
                if self.spec[0] == "RATING":
                    self.rating = self.spec[1]
                if self.spec[0] == "OPENED":
                    self.opened = self.spec[1]
                if self.spec[0] == "ADDED":
                    self.added = self.spec[1]
                if self.spec[0] == "NUMOPENED":
                    self.numopened = self.spec[1]
                if self.spec[0] == "LASTMOD":
                    self.lastmod = self.spec[1]
    def changeSpec(self, what, newSpec, how = None, listnum = None):
        if what == "ID":
            self.id = newSpec
            return True
        if what == "NAME":
            self.name = newSpec
            return True
        if what == "PATH":
            self.path = newSpec
            return True
        elif what == "GENRE":
            if how == "APPEND":
                self.genre.append(newSpec)
                return True
            elif how == "NEW":
                self.genre = []
                self.genre.append(newSpec)
                return True
            elif how == "CHANGE":
                if listnum < len(self.genre):
                    self.genre[listnum] = newSpec
                    return True
                #if given listindex is to big, report error
                else:
                    return False
            #if given how is no valid option, report error
            else:
                return  False
        elif what == "INTERPRET":
            if how == "APPEND":
                self.interpret.append(newSpec)
                return True
            elif how == "NEW":
                self.interpret = []
                self.interpret.append(newSpec)
                return True
            elif how == "CHANGE":
                if listnum < len(self.interpret):
                    self.interpret[listnum] = newSpec
                    return True
                #if given listindex is to big, report error
                else:
                    return False
            #if given how is no valid option, report error
            else:
                return  False
        if what == "STUDIO":
            self.studio = newSpec
            return True
        if what == "RATING":
            self.rating = newSpec
            return True
        if what == "OPENED":
            self.opened = newSpec
            return True
        if what == "ADDED":
            self.added = newSpec
            return True
        if what == "NUMOPENED":
            self.numopened = str(int(self.numopened)+1)
            return True
        if what == "LASTMOD":
            self.lastmod = newSpec
            return True
        #if given what is no calid option, report error
        else:
            return False
    def getSpec(self, what):
        if what == "ID$" or what == "ID":
            return self.id
        if what == "NAME$" or what == "NAME":
            return self.name
        if what == "PATH$" or  what =="PATH":
            return self.path
        if what == "GENRE$" or  what == "GENRE":
            return self.genre
        if what == "INTERPRET$" or what == "INTERPRET":
            return self.interpret
        if what == "STUDIO$" or what == "STUDIO":
            return self.studio
        if what == "RATING$" or what == "RATING":
            return self.rating
        if what == "OPENED$" or what == "OPENED":
            return self.opened
        if what == "ADDED$" or what == "ADDED":
            return self.added
        if what == "NUMOPENED$" or what == "NUMOPENED":
            return self.numopened
        if what == "LASTMOD$" or what == "LASTMOD":
            return self.lastmod
    def listofelements(self):
        self.loopelem = ["ID$","NAME$","PATH$","GENRE$","INTERPRET$","STUDIO$","RATING$","OPENED$","ADDED$","NUMOPENED$","LASTMOD$"]
        self.entrylist = []
        for elem in self.loopelem:
            if type(self.getSpec(elem)) is list:
                for subelem in self.getSpec(elem):
                    self.entrylist.append(elem)
                    self.entrylist.append(subelem)
                    self.entrylist.append(" ")
            elif elem == "ID$" or elem == "NUMOPENED$":
                self.entrylist.append(elem)
                self.entrylist.append(str(self.getSpec(elem)))
                self.entrylist.append(" ")
            else:
                self.entrylist.append(elem)
                self.entrylist.append(self.getSpec(elem))
                self.entrylist.append(" ")
        #self.entrylist = [str(self.__id),self.name,self.__path,]+self.genre+self.interpret
        #self.entrylist = [str(self.__id),self.name,self.__path,self.genre,self.interpret]
        return self.entrylist
    """
    #Old CODE
    def printentry(self, lenlist):
#        print self.id,self.name,self.path,' '.join(self.genre),(' '.join(self.interpret)).replace("%"," "),self.studio
        #Define look of output
        if int(self.id) <= 9:
            idprint = "  "+str(self.id)
        elif int(self.id) <= 99 and self.id > 9:
            idprint = " "+str(self.id)
        elif int(self.id) >= 100:
            idprint = str(self.id)
        if len(self.name) >= 20:
            nameprint = self.name[0:19]+".."
        elif len(self.name) < 20:
            nameprint = self.name +(21-len(self.name))*(" ")
        #Define what is shown:
        genreflag = False
        interpretflag = False
        studioflag = False
        genreprint = []
        for genre in self.genre:
            if genre != "nogenre":
                genreprint.append(genre)
                genreflag = True
        interpretprint = []
        for interpret in self.interpret:
            if interpret != "nointerpret":
                interpretprint.append(interpret)
                interpretflag = True
        studioprint = ""
        if self.studio != "nostudio":
            studioprint = self.studio
            studioflag = True
        if lenlist == None:
            printedstring = idprint+" "+nameprint+" "
            if genreflag == True:
                printedstring = printedstring+" "+' '.join(genreprint)
            if interpretflag == True:
                printedstring = printedstring+" "+(' '.join(interpretprint)).replace("%"," ")
            if studioflag == True:
                printedstring = printedstring+" "+studioprint
        else:
            printedstring = idprint+" "+nameprint
            printedgenre = ""
            printedinterpret = ""
            printedstudio = ""
            if genreflag == True:
                i = -1
                glen = 0
                for g in genreprint:
                    printedgenre = printedgenre + " " + g
                    glen = glen + len(g)
                    i = i + 1
                glen = glen + i
                #print glen, i
                if glen < lenlist[0][0]:
                    printedgenre = printedgenre + makestring(" ",lenlist[0][0]-glen)
            if genreflag == False:
                printedgenre = " " +  makestring(" ",lenlist[0][0])
            printedstring = printedstring + printedgenre
            if interpretflag == True:
                i = -1
                ilen = 0
                for inter in interpretprint:
                    printedinterpret = printedinterpret + " " + inter.replace("%"," ")
                    ilen = ilen + len(inter)
                    i = i + 1
                ilen = ilen + i
                if ilen < lenlist[1][0]:
                    printedinterpret = printedinterpret + makestring(" ",lenlist[1][0]-ilen)
            if interpretflag == False:
                printedinterpret = " " + makestring(" ",lenlist[1][0])
            printedstring = printedstring + printedinterpret
            if studioflag == True:
                printedstudio = " " + studioprint + makestring(" ",lenlist[2][0]-len(studioprint))
            if studioflag == False:
                printedstudio = " " + makestring(" ",lenlist[2][0])
            printedstring = printedstring + printedstudio
        print printedstring
        """

def main():
    DB1 = database(0,sys.argv[1])
    for i in range(len(DB1.entrys)):
        DB1.entrys[i].printentry()
    raw_input('taste druecken')
    DB1.removeentrys()
    for i in range(len(DB1.entrys)):
        DB1.entrys[i].printentry()

if __name__ == '__main__':
    main()
