from csv import writer, reader
from os import path, replace
from re import split
from sys import argv

from chardet.universaldetector import UniversalDetector

def Get_encoding(filepath):
    detector = UniversalDetector()
    for line in open(filepath, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']

def savepath(openpath: str):
    file_dir, filename = path.split(openpath)
    filename, file_ext = path.splitext(filename)
    return str(path.join(file_dir, filename))



if __name__ == "__main__":
