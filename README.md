xyz,dat文件格式转换

编译命令--带命令行窗口

`nuitka --standalone --lto=no --mingw64 --show-progress --show-memory
--nofollow-import-to=http,codes,logging,typing,enum,warings,ast,shutil,email,pandas,numpy,encodings
--include-module=ctypes --enable-plugin=pyside6 --output-dir=o main.py`

`nuitka --standalone --lto=no --mingw64 --show-progress --show-memory --enable-plugin=pyside6 --output-dir=t .\menu_ui.py`

编译命令--不带命令行窗口

`nuitka --standalone --lto=no --mingw64 --show-progress --show-memory
--nofollow-import-to=http,codes,logging,typing,enum,warings,ast,shutil,email,pandas,numpy,encodings
--include-module=ctypes --disable-console --enable-plugin=pyside6,upx --upx-binary="upx路径" --output-dir=o main.py`

`nuitka --standalone --lto=no --mingw64 --show-progress --show-memory --enable-plugin=pyside6,upx --disable-console --upx-binary="upx路径" --windows-uac-admin --output-dir=t .\menu_ui.py`

编译完成后 /o/main.dist和/t/main.dist下文件合并

合并后将/need文件夹下复制到上述合并的文件夹下

完成后用管理员身份运行menu_ui.exe，点击初始化即可添加Windows右键快捷方式
