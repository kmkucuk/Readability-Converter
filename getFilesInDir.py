# from os import walk
from os import walk, listdir

def getFilesInDir(mypath):
    f = []
    f = ['/'.join([mypath,file]) for file in listdir(mypath)]
    # for (dirpath, dirnames, filenames) in walk(mypath):
    #     f.extend('/'.join([mypath,list(filenames)[0]]))
    #     break
    return f

