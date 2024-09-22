# coding:utf-8
import winreg as reg
from os import path


def add_context_menu(menu_name, command, reg_root_key_path, reg_key_path, shortcut_key):
    """
    封装的添加一个右键菜单的方法
    :param menu_name: 显示的菜单名称
    :param command: 菜单执行的命令
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径（相对路径）
    :param shortcut_key: 菜单快捷键，如：'S'
    :return:
    """
    # 打开名称父键
    key = reg.OpenKey(reg_root_key_path, reg_key_path)
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name加上快捷键，数据类型为REG_SZ字符串类型
    reg.SetValue(key, menu_name, reg.REG_SZ, menu_name + '(&{0})'.format(shortcut_key))

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = reg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为command + ' "%v"'，数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key, 'command', reg.REG_SZ, command + ' "%v"')

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)


def delete_reg_key(root_key, key, menu_name):
    """
    删除一个右键菜单注册表子键
    :param root_key:根键
    :param key: 父键
    :param menu_name: 菜单子键名称
    :return: None
    """
    try:
        parent_key = reg.OpenKey(root_key, key)
    except Exception as msg:
        print(msg)
        return
    if parent_key:
        try:
            menu_key = reg.OpenKey(parent_key, menu_name)
        except Exception as msg:
            print(msg)
            return
        if menu_key:
            try:
                # 必须先删除子键的子键，才能删除子键本身
                reg.DeleteKey(menu_key, 'command')
            except Exception as msg:
                print(msg)
                return
            else:
                reg.DeleteKey(parent_key, menu_name)


def add_menu(z: float):
    """
    添加右键菜单，可以在右键点击一个文件、目录、文件夹空白处或驱动器盘符后在命令行中打印出当前的绝对路径
    :return: None
    """

    # 添加文件右键菜单
    add_context_menu('转换为XYZ', path.dirname(__file__) + '\main.exe -mode xyz',
                     reg.HKEY_CLASSES_ROOT, r'*\\shell',
                     'S')
    add_context_menu('转换为DAT', path.dirname(__file__) + '\main.exe -mode dat',
                     reg.HKEY_CLASSES_ROOT, r'*\\shell',
                     'S')
    add_context_menu('转换为XYZ并转换高程', path.dirname(__file__) + '\main.exe -mode xyz --c {}'.format(z),
                     reg.HKEY_CLASSES_ROOT,
                     r'*\\shell',
                     'S')
    add_context_menu('交换XY', path.dirname(__file__) + '\main.exe -mode xyz --swap 1',
                     reg.HKEY_CLASSES_ROOT,
                     r'*\\shell',
                     'S')
    add_context_menu('Z值取反', path.dirname(__file__) + '\main.exe -mode xyz --t 1',
                     reg.HKEY_CLASSES_ROOT,
                     r'*\\shell',
                     'S')
    # 添加文件夹右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\shell', 'S')
    # 添加文件夹空白处右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', 'S')
    # 添加磁盘驱动器右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Drive\\shell', 'S')


def delete_all_menu():
    menu_name = ['转换为DAT', '转换为XYZ', '转换为XYZ并转换高程', '交换XY', 'Z值取反']
    for i in menu_name:
        delete_reg_key(reg.HKEY_CLASSES_ROOT, r'*\\shell', i)
        # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\shell', menu_name)
        # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', menu_name)
        # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Drive\\shell', menu_name)
