from PySide6.QtWidgets import QMessageBox, QApplication

app = QApplication([])
QMessageBox.critical(None, "错误", "请输入文件路径")
