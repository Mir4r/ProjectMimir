#Functions and stuff, that is needed by different parts of Project Mimir
#2014, K. Schweiger
import os
import sys

def readFile(directory, filename):
    charset = sys.getfilesystemencoding()
    lines = []
    #read config and test if it exists
    try:
        open(os.path.join(directory,filename), 'r')
    except IOError:
        print filename+" does not exist"
        return False
    with open(os.path.join(directory,filename), 'r') as f:
        inputfile = f.read()
    #after this you have one sting with all lines seperatet by \n
    #so split it! -> lines is a list with the lines from the read file
    lines = inputfile.split("\n")
    return lines

def savefile(directory, filename, backupflag):
    if backupflag == True:
        backupfile(directory, filename)
    print "Saving file..."
    

def backupfile(directory, filename):
    print "Backing up file..."
    os.system("cp "+os.path.join(directory, filename)+" "+filename+".backup")


def gettime(flag):
    lt = time.localtime()
    if flag == "date":
        if int(lt[2]) <= 9:
            dateres = "0"+str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        else:
            dateres = str(lt[2])+"."+str(lt[1])+"."+str(lt[0]-2000)
        return dateres
    elif flag == "time":
        timeres = str(lt[3])+":"+str(lt[4])+":"+str(lt[5])
        return timeres
