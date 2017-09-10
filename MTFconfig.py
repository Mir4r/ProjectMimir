#Collection of operations on the MTF config
#2015, K Schweiger
import os
import sys
import sharedfunctions

#returns a list. With following entrys:
#0: A list with specs that should be printed
def configreader(workdir):
    lines = sharedfunctions.readFile(workdir, 'MTF.cfg')
    config = {}
    for line in lines:
        #ignore Lines beginning with # or nothing in it
        #Define keys and seperators for config elements
        configkeys = {"printspec="     : [",",  "str"],
                      "showspec="      : [",",  "str"],
                      "numtoprint="    : [None, "int"],
                      "maxnamelen="    : [None, "int"],
                      "openedacc="     : [None, "str"],
                      "termwidth="     : [None, "int"],
                      "termheight="    : [None, "int"],
                      "nGenre="        : [None, "int"],
                      "genrePriority=" : [",",  "str"],
                      "invisibleGenre=": [",",  "str"]}
        
        if len(line) > 0 and line[0] != "#":
            for key in configkeys:
                if line.startswith(key):
                    if configkeys[key][0] is not None:
                        config.update({key : line[len(key)::].split(configkeys[key][0])})
                    else:
                        if configkeys[key][1] is "str":
                            config.update({key : str(line[len(key)::])})
                        elif configkeys[key][1] is "int":
                            config.update({key : int(line[len(key)::])})

    return config


def getconfigpart(workdir, cfg):
    config = configreader(workdir)
    if cfg == "SpecsToPrint":
        return config["printspec="]
    elif cfg == "SpecsToShow":
        return config["showspec="]
    elif cfg == "NumToPrint":
        return config["numtoprint="]
    elif cfg == "MaxNameLen":
        return config["maxnamelen="]
    elif cfg == "DateAcc":
        return config["openedacc="]
    elif cfg == "GenrePriority":
        return config["genrePriority="]
    elif cfg == "NumberofGenres":
        return config["nGenre="]
    elif cfg == "TerminalWidth":
        return config["termwidth="]
    elif cfg == "TerminalHeight":
        return config["termheight="]
    elif cfg == "InvisibleGenres":
        return config["invisibleGenre="]
