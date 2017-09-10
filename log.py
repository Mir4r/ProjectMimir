RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
ENDC = '\033[0m'

def disable():
    RED = ''
    BLUE = ''
    GREEN = ''
    ENDC = ''

def printred ( msg):
    print RED + msg + ENDC

def printgreen( msg):
    print GREEN + msg + ENDC

def printblue( msg):
    print BLUE + msg + ENDC

