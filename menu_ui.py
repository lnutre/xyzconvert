from PySide6.QtWidgets import QPushButton, QWidget, QMessageBox, QMainWindow, QVBoxLayout, QApplication, QLabel, \
    QHBoxLayout, QLineEdit
from menu import delete_all_menu, add_menu

import platform


class Mainwidows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("程序初始化")
        # 创建按钮
        self.z_label = QLabel('高程转换值:')
        self.z = QLineEdit()
        self.init_button = QPushButton("初始化")
        self.clean_button = QPushButton("清除快捷方式")
        self.exec_button = QPushButton("退出")

        hlayout=QHBoxLayout()
        hlayout.addWidget(self.z_label)
        hlayout.addWidget(self.z)

        # 创建垂直布局
        vlayout = QVBoxLayout()

        # 将按钮添加到布局
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.init_button)
        vlayout.addWidget(self.clean_button)
        vlayout.addWidget(self.exec_button)

        # 将布局设置为主窗口的中央部分
        central_widget = QWidget()
        central_widget.setLayout(vlayout)
        self.setCentralWidget(central_widget)

        # 连接按钮的点击信号到槽函数
        self.init_button.clicked.connect(self.add_menu)
        self.clean_button.clicked.connect(self.clean_menu)
        self.exec_button.clicked.connect(self.close)

    def add_menu(self):
        add_menu(float(self.z.text()))

    def clean_menu(self):
        delete_all_menu()


if __name__ == "__main__":
    app = QApplication([])

    example = Mainwidows()
    example.show()

    app.exec()
