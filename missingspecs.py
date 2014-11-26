#!/usr/bin/env python
#Script for adding ned specs to existing DB.
#2014, Korbinian Schweiger

import os
import sys
import backend

def addspec(name, value, workdir):
    lines = readDB(workdir)
    for i in range(len(lines)):
        print lines[i]
        lines[i] = lines[i] + name +"$"+value+" "
        print lines[i]
    print lines
    saveDB(workdir, lines)

def readDB(directory):
    charset = sys.getfilesystemencoding()
    lines = []
    #read file "main.db" in the starting directory (dirs[0])
    try:
        open(os.path.join(directory, 'main.db'), 'r')
    except IOError:
        print "The Database does not exist"
        return False
    with open(os.path.join(directory, 'main.db'), 'r') as f:
        input = f.read()
    #after this you have one sting with all lines seperatet by \
    #so split it! -> self.lines is a list with the lines from the read file
    lines = input.split("\n")
    lines.pop()        
    return lines

def saveDB(workdir, lines):
    charset = sys.getfilesystemencoding()
    with open(os.path.join(workdir, 'main.db'), 'w+') as f:
        for line in lines:
            write_items = f.write(line)
            write_items = f.write("\n")


def main(workdir):
    print "Project Mimir: Script for adding new spacs to a old Database"
    #workdir = raw_input("Input the directory of the DB: ")
    newspecnum = int(raw_input("Input number of spec to be added? "))
    DBspecs = backend.getcurrentspecs()
    for i in range(newspecnum):
        newspec = raw_input("Input new spec name: ")
        if newspec in DBspecs:
            newvalue = raw_input("Input the standardvalue for the new spec: ")
            addspec(newspec,newvalue,workdir)

if __name__ == '__main__':
    main()
