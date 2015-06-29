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
    return RED + msg + ENDC

def green( msg):
    return GREEN + msg + ENDC

def blue( msg):
    return BLUE + msg + ENDC

