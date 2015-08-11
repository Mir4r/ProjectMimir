#Collection of operations on the MTF config
#2015, K Schweiger
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
            elif line[0:9] == "showspec=":
                config.append(line[9::].split(","))
            elif line[0:11] == "numtoprint=":
                config.append(int(line[11::]))
            elif line[0:11] == "maxnamelen=":
                config.append(int(line[11::]))
            elif line[0:10] == "openedacc=":
                config.append(line[10::])
    return config


def getconfigpart(workdir, cfg):
    config = configreader(workdir)
    if cfg == "SpecsToPrint":
        return config[0]
    elif cfg == "SpecsToShow":
        return config[1]
    elif cfg == "NumToPrint":
        return config[2]
    elif cfg == "MaxNameLen":
        return config[3]
    elif cfg == "DateAcc":
        return config[4]
