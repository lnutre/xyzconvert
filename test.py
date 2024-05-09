import csv, threading, queue, time
from _csv import writer, reader

from chardet.universaldetector import UniversalDetector
from re import split
from os import path

filepath = r"C:\Users\Administrator\Desktop\xha-10m.xyz"


def Get_encoding(filepath):
    detector = UniversalDetector()
    for line in open(filepath, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']

print(path.dirname(__file__))

with open(r"C:\Users\Administrator\Desktop\1", "a", encoding='utf-8', newline="") as f:
    csv_writer = writer(f)
    n = 1
    with open(r"C:\Users\Administrator\Desktop\1.xyz", 'r', encoding='utf-8') as c:
        clist = reader(c)
        for line in clist:
            line.insert(0, '')
            line.insert(0, str(n))
            n += 1
            print(line)
            csv_writer.writerow(line)
f.close()

dir = str(1)
filename = str(1) + '.xyz'
print(path.join(dir, filename))
