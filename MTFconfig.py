#Collection of operations on the MTF config
#2014, K Schweiger
import os
import sys
import sharedfunctions

#returns a list. With following entrys:
#0: A list with specs that should be printed
def configreader(workdir):
    lines = sharedfunctions.readFile(workdir, 'MTF.cfg')
    config = []
    for line in lines:
        #ignore Lines beginning with # or nothing in it
        if len(line) > 0 and line[0] != "#":
            if line[0:10] == "printspec=":
                config.append(line[10::].split(","))
    return config


def getconfigpart(workdir, cfg):
    config = configreader(workdir)
    if cfg == "SpecsToPrint":
        return config[0]
