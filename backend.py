#!/usr/bin/env python
#2014, Korbinian Schweiger


import sys
import os
from glob import glob

def getVersion():
    return "v0.1.1"


class database:
    def __init__(self,flag,startdir):
        self.entrys = []
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
                self.entrys.append(entry(None, self.id, os.path.splitext(os.path.basename(foundfiles))[0], foundfiles, "genre","interpret","nostudio","notrated"))
                self.id = self.id + 1
        if flag == 1:
            self.dirs = [startdir]
            self.DBlines = self.readDB(startdir)
            for lines in self.DBlines:
                self.specs = []
                self.specs = lines.split(" ")
                self.entrys.append(entry(self.specs))
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
    #Read the Database file and returns a list of the lines in the file
    def readDB(self, directory):
        print "ReadDB"
        #open file
        charset = sys.getfilesystemencoding()
        self.lines = []
        #read file "main.db" in the starting directory (dirs[0])
        with open(os.path.join(directory, 'main.db'), 'r') as f:
            self.input = f.read()
        #after this you have one sting with all lines seperatet by \n
        #so split it! -> self.lines is a list with the lines from the read file
        self.lines = self.input.split("\n")
        self.lines.pop()
        return self.lines
    def addentry(self, name, path, genre, interpret, studio,rating):
        print "A new Entry will be added to the DB"
        self.id = len(self.entrys) 
        self.entrys.append(entry(None,self.id,name,path,genre,interpret,studio,rating))

    def modifyentry(self, changewhat, change, startid, endid = None, changeindex = None, changehow = None):
        self.index = startid
        if changeindex is None and changehow is None:
            if endid is None:
                self.endindex = self.index
            else:
                self.endindex = endid
            while(self.index <= self.endindex):
                self.entrys[self.index].changeSpec(changewhat,change)
                self.index = self.index + 1
            print self.entrys[0].name
        else:
            if endid is None:
                self.endindex = self.index
            else:
                self.endindex = endid
            while(self.index <= self.endindex):
                self.status = self.entrys[self.index].changeSpec(changewhat,change,changehow,changeindex)
                self.index = self.index + 1
                if self.status == False:
                    print "Soming went wrong for your modifing request of entry ",self.index
        #call changeing methode for the entry, that should be changed
    #Method for saving the filelist
    def saveDB(self):
        charset = sys.getfilesystemencoding()
        #write a file "fileslist" in the starting directory (dirs[0])
        with open(os.path.join(self.dirs[0].decode(charset), 'main.db'), 'w+') as f:
            for e in self.entrys:
                write_items = f.write(''.join(e.listofelements()))
                write_items = f.write("\n")
    def printbycriteria(self, criterialist):
        for i in range(len(self.entrys)):
            self.toprint = []
            self.printflag = False
            for criteria in criterialist:
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
                self.toprint.append(self.flag)
            #print self.toprint
            #print self.toprint
            self.printflag = True
            for j in range(len(self.toprint)):
                if self.toprint[j] == False:
                    self.printflag = False
            if self.printflag == True:
                self.entrys[i].printentry()
    def findnewfiles(self, startdir):
      self.dirs = self.dirfinder(startdir)
      #filelist contains the paths to the files
      self.filelist = []
      for d in self.dirs:
          self.filelist = self.filelist + self.getfiles(d)
      for foundfile in self.filelist:
          self.existflag = False
          for i in range(len(self.entrys)):
              #print self.entrys[i].getSpec("PATH")
              if self.entrys[i].getSpec("PATH") == foundfile:
                  self.existflag = True
          if self.existflag == False:
              print foundfile
              self.id = len(self.entrys) 
              self.entrys.append(entry(None,self.id,os.path.splitext(os.path.basename(foundfile))[0], foundfile, "genre","interpret","nostudio","notrated"))
    def runentry(self, entryid):
        os.system("vlc "+str(self.entrys[entryid].getSpec("PATH"))) 
    def getnumberofentrys(self):
        return len(self.entrys)
        

class entry:
    def __init__(self, specs, id=None, name=None, path=None, genre=None, interpret=None, studio=None, rating=None):
        if specs is None:
            self.genre = []
            self.interpret = []
            self.__id=id
            self.name=name
            self.__path=path
            self.genre.append(genre)
            self.interpret.append(interpret)
            self.studio=studio
            self.rating=rating
        else:
            self.genre = []
            self.interpret = []        
            for num in specs:
                self.spec = num.split('$')
                if self.spec[0] == "ID":
                    self.__id = self.spec[1]
                if self.spec[0] == "NAME":
                    self.name = self.spec[1]
                if self.spec[0] == "PATH":
                    self.__path = self.spec[1]
                if self.spec[0] == "GENRE":
                    self.genre.append(self.spec[1])
                if self.spec[0] == "INTERPRET":
                    self.interpret.append(self.spec[1])  
                if self.spec[0] == "STUDIO":
                    self.studio = self.spec[1]
                if self.spec[0] == "RATING":
                    self.rating = self.spec[1]
    def changeSpec(self, what, newSpec, how = None, listnum = None):
        if what == "NAME":
            self.name = newSpec
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
        #if given what is no calid option, report error
        else:
            return False
    def getSpec(self, what):
        if what == "ID$" or what == "ID":
            return self.__id
        if what == "NAME$" or what == "NAME":
            return self.name
        if what == "PATH$" or  what =="PATH":
            return self.__path
        if what == "GENRE$" or  what == "GENRE":
            return self.genre
        if what == "INTERPRET$" or what == "INTERPRET":
            return self.interpret
        if what == "STUDIO$" or what == "STUDIO":
            return self.studio
        if what == "RATING$" or what == "RATING":
            return self.rating        
    def listofelements(self):
        self.loopelem = ["ID$","NAME$","PATH$","GENRE$","INTERPRET$","STUDIO$","RATING$"]
        self.entrylist = []
        for elem in self.loopelem:
            if type(self.getSpec(elem)) is list:
                for subelem in self.getSpec(elem):
                    self.entrylist.append(elem)
                    self.entrylist.append(subelem)
                    self.entrylist.append(" ")
            elif elem == "ID$":
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
    def printentry(self):
        print self.__id,self.name,' '.join(self.genre),(' '.join(self.interpret)).replace("%"," "),self.studio

def main():
    DB1 = database(1,sys.argv[1])
    #for i in range(len(DB1.entrys)): 
    #    DB1.entrys[i].printentry()
    #DB1.printbycriteria(["genre1","interpret1"])
    #print "HALLO"
    #DB1.runentry(0)
    #DB1.findnewfiles(sys.argv[1])
    #print DB1.entrys[0].getSpec("GENRE")
    #DB1.printbyGenre("genre1")
#    for i in range(len(DB1.entrys)): 
 #       DB1.entrys[i].printentry()
    #DB1.entrys[2].changegenre("GENRE",0,0)
    #print "\n"
    #for i in range(len(DB1.entrys)):
    #    DB1.entrys[i].printentry()
    #DB1.saveDB() 
    #print DB1.getnumberofentrys()

if __name__ == '__main__':
    main()



