# from os import walk
from os import walk, listdir

def getFiles(mypath):
    f = []
    f = ['\\'.join([mypath,file]) for file in listdir(mypath)]
    return f

