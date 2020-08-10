import os
import pathlib

os.chdir(pathlib.Path(__file__).parent.parent.absolute())


def read(path):
    with open(path) as f:
        data = f.read()
    return data


def write(path, data):
    with open(path) as f:
        f.write(data)


def getStream(path):
    return open(path)
