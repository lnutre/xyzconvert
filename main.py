import argparse
from os import path
import pandas as pd
from chardet.universaldetector import UniversalDetector
from PySide6.QtWidgets import QMessageBox, QApplication


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
        data.to_csv(str(path.join(file_dir, filename)), header=False, float_format='%.2f', index=False)
    elif mode == 'dat':
        data.insert(0, 'name', "")
        # print(data)
        data.to_csv(str(path.join(file_dir, filename)), header=False, float_format='%.2f')
        # np.savetxt(str(path.join(file_dir, filename)), data, delimiter=',')


def openfile(openpath: str):
    data = pd.read_csv(openpath, sep=r'\t|,| |  |\s+', encoding=Get_encoding(openpath), header=None, engine='python')
    data.dropna(axis=1, how='all', inplace=True)
    data = data.iloc[:, -3:]
    data.columns = ['X', 'Y', 'Z']
    return data


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("-mode", help="转换类型", choices=['xyz', 'dat'])
    parse.add_argument("filepath", help="文件路径")
    parse.add_argument("--swap", help="交换xy")
    parse.add_argument("--c", help="z加减数值")
    args = parse.parse_args()
    # print(args.filepath)
    app = QApplication([])
    if args.filepath:
        if args.c:
            data = openfile(args.filepath)
            data['Z'] = data['Z'].map(lambda x: x + float(args.c))
            savefile(data, args.filepath, args.mode)
            QMessageBox.information(None, "通知", "转换完成")
        else:
            savefile(openfile(args.filepath), args.filepath, args.mode)
            QMessageBox.information(None, "通知", "转换完成")
        if args.swap:
            data = openfile(args.filepath)
            data[['X', 'Y', 'Z']] = data[['Y', 'X', 'Z']]
            savefile(data, args.filepath, args.mode)
            QMessageBox.information(None, "通知", "转换完成")
    else:
        QMessageBox.critical(None, "错误", "请输入文件路径")
