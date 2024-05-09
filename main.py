import argparse
import re
import sys
from os import path,system
import numpy as np
from pandas import DataFrame
from chardet.universaldetector import UniversalDetector
from sys import argv


def Get_encoding(filepath):
    detector = UniversalDetector()
    for line in open(filepath, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


def savefile(data, openpath: str, mode: str):
    file_dir, filename = path.split(openpath)
    filename, file_ext = path.splitext(filename)
    filename = filename + '.' + mode
    if mode == "xyz":
        np.savetxt(str(path.join(file_dir, filename)), data, delimiter=',', fmt="%.2f")
    elif mode == 'dat':
        data = DataFrame(data)
        data.insert(0, 'name', "")
        # print(data)
        data.to_csv(str(path.join(file_dir, filename)), header=False)
        # np.savetxt(str(path.join(file_dir, filename)), data, delimiter=',')


def custom_split(line):
    print(type(line))
    print(list(map(float, re.split("[ ,\t]", line))))
    return np.array(list(map(float, re.split("[ ,\t]", line))), dtype=float)


def openfile(openpath: str):
    data = np.fromregex(openpath, regexp=r'(\b\d+\.*\d*\b)(\D)(\b\d+\.*\d*\b)(\D)(\b\d+\.*\d*\b)',
                        encoding=Get_encoding(openpath),
                        dtype=[('x', float), ('F1', str), ('y', float), ('F2', str), ('z', float)])
    data = np.vstack((data['x'], data['y'], data['z'])).T
    return data


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-mode", help="转换类型", choices=['xyz', 'dat'])
    parse.add_argument("filepath", help="文件路径")
    parse.add_argument("--swap", help="交换xy")
    parse.add_argument("--c", help="z加减数值")
    args = parse.parse_args()
    # print(args.filepath)
    if args.filepath:
        if args.c:
            data = openfile(args.filepath)
            data[:, -1] = data[:, -1] + float(args.c)
            savefile(data, args.filepath, args.mode)
        else:
            savefile(openfile(args.filepath), args.filepath, args.mode)
        if args.swap:
            data = openfile(args.filepath)
            data = data[:, [1, 0, 2]]
            savefile(data, args.filepath, args.mode)
    else:
        print("请输入文件路径")
