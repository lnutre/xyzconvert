import queue
import threading
from csv import writer, reader
from os import path, replace
from re import split
from sys import argv

from chardet.universaldetector import UniversalDetector

t = 1


def Get_encoding(filepath):
    detector = UniversalDetector()
    for line in open(filepath, 'rb'):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']


def processing(q, anti=None, dH: float = None) -> list:
    q = q.get()
    q[-1] = str(round((float(q[-1]) + dH) * anti, 2))
    return q


def savepath(openpath: str):
    file_dir, filename = path.split(openpath)
    filename, file_ext = path.splitext(filename)
    return str(path.join(file_dir, filename))


class convertxyz(threading.Thread):
    def __init__(self, q, path1: str, anti1=None, dH1: float = None):
        threading.Thread.__init__(self)
        self.savepath = path1
        self.q = q
        self.anti = anti1
        self.dH = float(dH1)

    def run(self):
        while True:
            try:
                mutx.acquire()
                with open(self.savepath + '.xyz', 'a', encoding='utf-8', newline="") as file:
                    csv_writer1 = writer(file)

                    csv_writer1.writerow(processing(self.q, self.anti, self.dH))
                mutx.release()
            except:
                break


class convertdat(threading.Thread):
    def __init__(self, q, path1: str, anti1=None, dH1: float = None):
        threading.Thread.__init__(self)
        self.savepath = path1
        self.q = q
        self.anti = anti1
        self.dH = float(dH1)

    def run(self):
        global t
        while True:
            try:
                mutx.acquire()
                with open(self.savepath + '.dat', 'a', encoding='utf-8', newline="") as file:
                    csv_writer1 = writer(file)
                    l = processing(self.q, self.anti, self.dH)
                    l.insert(0, '')
                    l.insert(0, str(t))
                    csv_writer1.writerow(l)
                t += 1
                mutx.release()
            except:
                break


if __name__ == "__main__":

    thread_num = int(argv[1])
    openpath = str(argv[2])
    print(openpath)
    dH = float(argv[3])
    mode = argv[4]
    anti = argv[5]
    if int(anti) == 0:
        anti = 1
    else:
        anti = -1
    mutx = threading.Lock()
    doqueue = queue.Queue(maxsize=0)
    for line in open(openpath, 'r', encoding=Get_encoding(openpath)):
        r = split(" |,|\t|\n", line.strip())
        r = r[-3:]
        doqueue.put(r)

    if mode == "xyz":
        threads = []
        for i in range(thread_num):
            thread = convertxyz(doqueue, savepath(openpath), anti, dH)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    elif mode == 'dat':
        threads = []
        for i in range(thread_num):
            thread = convertdat(doqueue, savepath(openpath), anti, dH)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    else:
        replace(savepath(openpath), openpath)
    print("end")
