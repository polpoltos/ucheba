from PyQt6.QtWidgets import QFileDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QApplication, QMainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import sys
import subprocess


class MyWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(562, 571)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 521, 511))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(parent=self.widget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 562, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.open_file_dialog)
        self.pushButton_2.clicked.connect(self.save_file)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton.setText(_translate("MainWindow", "Open"))

    def open_file_dialog(self):
        # Получаем путь к директории, где лежит текущий файл
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Открываем диалоговое окно для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", current_dir, "Text Files (*.txt)")

        if file_name:
            print(f"Выбран файл: {file_name}")
            # Открываем файл с помощью Notepad
            subprocess.run(['notepad', file_name])

            # Читаем содержимое файла
            with open(file_name, 'r') as file:
                self.content = file.read()
                print(f"Содержимое файла: {self.content}")
        else:
            print("Файл не выбран.")

    def save_file(self):
        # Получаем имя файла из поля ввода
        file_name = self.input_field.text()

        # Если имя файла не пустое, сохраняем файл
        if file_name:
            with open(file_name + '.txt', 'w') as file:
                file.write("Это пример текста.")
            print(f"Файл '{file_name}.txt' успешно сохранен.")
        else:
            print("Введите имя файла.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = MyWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())