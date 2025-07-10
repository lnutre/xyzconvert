# coding:utf-8
import winreg as reg
from os import path
import platform

def add_context_menu_parent(parent_name, reg_root_key_path, reg_key_path, shortcut_key):
    """
    添加一级右键菜单
    :param parent_name: 一级菜单名称
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径
    :param icon_path: 菜单图标路径
    :param shortcut_key: 菜单快捷键
    """
    try:
        key = reg.OpenKey(reg_root_key_path, reg_key_path, 0, reg.KEY_ALL_ACCESS)
    except Exception as msg:
        key = reg.CreateKey(reg_root_key_path, reg_key_path)
    reg.SetValueEx(key, 'MUIVerb', 0, reg.REG_SZ, parent_name + '(&{0})'.format(shortcut_key))
    reg.SetValueEx(key, 'Default', 0, reg.REG_SZ, '')
    reg.SetValueEx(key, 'SubCommands', 0, reg.REG_SZ, '')
    reg.CloseKey(key)

def add_context_menu(menu_name, command, reg_root_key_path, reg_key_path):
    """
    添加二级右键菜单项
    :param menu_name: 二级菜单名称
    :param command: 菜单执行的命令
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径
    :param icon_path: 菜单图标路径
    """
    try:
        key = reg.OpenKey(reg_root_key_path, reg_key_path,0, reg.KEY_ALL_ACCESS)
    except Exception as msg:
        key = reg.CreateKey(reg_root_key_path, reg_key_path)
    reg.SetValueEx(key, 'MUIVerb', 0, reg.REG_SZ, menu_name)
    reg.SetValue(key, 'command', reg.REG_SZ, command+ ' "%v"')
    reg.CloseKey(key)

def delete_reg_key(root_key, sub_key):
    """
    删除一个右键菜单注册表子键
    :param root_key:根键
    :param sub_key: 父键
    :return: None
    """
    try:
        # 打开指定的注册表键
        with reg.OpenKey(root_key, sub_key, 0, reg.KEY_ALL_ACCESS) as key:
            # 获取子键数量
            info = reg.QueryInfoKey(key)
            num_sub_keys = info[0]

            # 递归删除所有子键
            for i in range(num_sub_keys - 1, -1, -1):
                sub_key_name = reg.EnumKey(key, i)
                delete_reg_key(root_key, f"{sub_key}\\{sub_key_name}")

        # 删除当前键
        reg.DeleteKey(root_key, sub_key)
        print(f"删除: {sub_key}")
    except FileNotFoundError:
        print(f"该y {sub_key} 不存在.")
    except PermissionError:
        print(f"你没有权限删除 {sub_key}.请以管理员身份运行")
    except Exception as e:
        print(f"删除时发生错误 {sub_key}: {e}")

def add_menu(z: float):
    """
    添加右键菜单，可以在右键点击一个文件、目录、文件夹空白处或驱动器盘符后在命令行中打印出当前的绝对路径
    :return: None
    """
    if platform.system() == 'Windows':
        if int(platform.version().split('.')[2]) >= 22000:
            add_context_menu_parent('xyz转换工具', reg.HKEY_CLASSES_ROOT, r'*\\shell\\xyzcon', 'C')
            add_context_menu('转换为XYZ', path.dirname(__file__) + '\main.exe -mode xyz', reg.HKEY_CLASSES_ROOT, r'*\\shell\\xyzcon\\shell\\2xyz')
            add_context_menu('转换为DAT', path.dirname(__file__) + '\main.exe -mode dat', reg.HKEY_CLASSES_ROOT, r'*\\shell\\xyzcon\\shell\\2dat')
            add_context_menu('转换为XYZ并转换高程', path.dirname(__file__) + '\main.exe -mode xyz --c {}'.format(z),
                             reg.HKEY_CLASSES_ROOT,
                             r'*\\shell\\xyzcon\\shell\\2h')
            add_context_menu('交换XY', path.dirname(__file__) + '\main.exe -mode xyz --swap 1',
                             reg.HKEY_CLASSES_ROOT,
                             r'*\\shell\\xyzcon\\shell\\swapxy')

        else:
            # 添加文件右键菜单
            add_context_menu('转换为XYZ', path.dirname(__file__) + '\main.exe -mode xyz', reg.HKEY_CLASSES_ROOT, r'*\\shell\\转换为XYZ')
            add_context_menu('转换为DAT', path.dirname(__file__) + '\main.exe -mode dat', reg.HKEY_CLASSES_ROOT, r'*\\shell\\转换为DAT')
            add_context_menu('转换为XYZ并转换高程', path.dirname(__file__) + '\main.exe -mode xyz --c {}'.format(z),
                             reg.HKEY_CLASSES_ROOT,
                             r'*\\shell\\转换为XYZ并转换高程')
            add_context_menu('交换XY', path.dirname(__file__) + '\main.exe -mode xyz --swap 1',
                             reg.HKEY_CLASSES_ROOT,
                             r'*\\shell\\交换XY')
    # 添加文件夹右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\shell', 'S')
    # 添加文件夹空白处右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', 'S')
    # 添加磁盘驱动器右键菜单
    # add_context_menu(menu_name, py_command, reg.HKEY_CLASSES_ROOT, r'Drive\\shell', 'S')


def delete_all_menu():
    if platform.system() == 'Windows':
        if int(platform.version().split('.')[2]) >= 22000:
            delete_reg_key(reg.HKEY_CLASSES_ROOT, r'*\\shell\\xyzcon')
        else:
            menu_name = ['转换为DAT', '转换为XYZ', '转换为XYZ并转换高程', '交换XY']
            for i in menu_name:
                delete_reg_key(reg.HKEY_CLASSES_ROOT, r'*\\shell'+i)
                # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\shell', menu_name)
                # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Directory\\Background\\shell', menu_name)
                # delete_reg_key(reg.HKEY_CLASSES_ROOT, r'Drive\\shell', menu_name)
