import os
from genericpath import exists

def create(dirName):
    try:
        if not exists(dirName):
            os.mkdir(dirName)
    except OSError as error:
        print(error)