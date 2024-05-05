import argparse
from os import path
import numpy as np
from chardet.universaldetector import UniversalDetector


def Get_encoding(filepath):
    detector = UniversalDetector()
    for line in open(filepath, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


def savefile(data, openpath: str, mode):
    file_dir, filename = path.split(openpath)
    filename, file_ext = path.splitext(filename)
    file_ext = '.' + mode
    np.savetxt(str(path.join(path.join(file_dir, filename), file_ext)), data, delimiter=',', fmt="%.2f")
    return str(path.join(path.join(file_dir, filename), file_ext))


def openfile(openpath: str):
    data = np.loadtxt(openpath, delimiter=" ,\t", encoding=Get_encoding(openpath))
    data = data[:, -3:-1]
    return data


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("filepath", help="文件路径")
    parse.add_argument("-mode", help="转换类型", choices=['xyz', 'dat'])
    parse.add_argument("--c", help="调整数值")
    args = parse.parse_args()
    if args.filepath:
        if args.c:
            print(0)
        else:
            savefile(openfile(args.filepath), args.filepath, args.mode)
    else:
        print("请输入文件路径")
