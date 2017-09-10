RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
ENDC = '\033[0m'

def disable():
    RED = ''
    BLUE = ''
    GREEN = ''
    ENDC = ''

def red ( msg):
    return RED + str(msg) + ENDC

def green( msg):
    return GREEN + str(msg) + ENDC

def blue( msg):
    return BLUE + str(msg) + ENDC
