from PySide6.QtWidgets import QMessageBox, QApplication
import platform
import winreg as reg

print(platform.system())
print(int(platform.version().split('.')[2])<20000)


if reg.OpenKey(reg.HKEY_CLASSES_ROOT, r'*\\shell\\xyzcon'):
    print("yes")
else:
    print("no")