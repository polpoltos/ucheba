import sys
from PyQt6.QtWidgets import QApplication, QDialog, QWidget, QMainWindow
from design import Ui_Lab_1

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_Lab_1()
ui.setupUi(window)
window.show()
sys.exit(app.exec())