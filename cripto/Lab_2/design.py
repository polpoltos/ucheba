import sys
from PyQt6 import QtCore, QtWidgets
from math import log2
from PyQt6.QtWidgets import QFileDialog
import os
import subprocess

editorProgram = 'notepad'                                            # notepad

class Ui_Lab_1(object):
    def __init__(self):
        super().__init__()
        self.radio_value = 1
        self.txt = open('3.txt', 'r+')
        self.text_txt = self.txt.read()

    def setupUi(self, Lab_1):
        Lab_1.setObjectName("Lab_1")
        Lab_1.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=Lab_1)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 110, 611, 264))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(parent=self.widget)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.textEdit = QtWidgets.QTextEdit(parent=self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.widget1 = QtWidgets.QWidget(parent=self.splitter)
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(parent=self.widget1)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(parent=self.widget1)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_2.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(parent=self.widget1)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_2.addWidget(self.radioButton_3)
        self.textEdit_2 = QtWidgets.QTextEdit(parent=self.splitter)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        Lab_1.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Lab_1)
        self.statusbar.setObjectName("statusbar")
        Lab_1.setStatusBar(self.statusbar)

        self.retranslateUi(Lab_1)
        QtCore.QMetaObject.connectSlotsByName(Lab_1)

        self.radio_function()
        self.push_button1_func()
        self.push_button2_func()

    def retranslateUi(self, Lab_1):
        _translate = QtCore.QCoreApplication.translate
        Lab_1.setWindowTitle(_translate("Lab_1", "Lab_1"))
        self.radioButton.setText(_translate("Lab_1", "Kirilitsa"))
        self.radioButton_2.setText(_translate("Lab_1", "Латиница"))
        self.radioButton_3.setText(_translate("Lab_1", "!№*#"))
        self.pushButton.setText(_translate("Lab_1", "Подсчёт"))
        self.pushButton_2.setText(_translate("Lab_1", "Изменение словаря"))

    def open_file_dialog(self):
        # Получаем путь к директории, где лежит текущий файл
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Открываем диалоговое окно для выбора файла
        file, _ = QFileDialog.getOpenFileName(None, "Open File", current_dir, "Text Files (*.txt)")

        subprocess.run(['notepad', file])
    def radio_function(self):
        self.radioButton.clicked.connect(lambda: self.radio(1))
        self.radioButton_2.clicked.connect(lambda: self.radio(2))
        self.radioButton_3.clicked.connect(lambda: self.radio(3))

    def radio(self, value):
        self.radio_value = value

    def push_button1_func(self):
        self.pushButton.clicked.connect(self.push_b1)

    def push_b1(self):
        stroka = str(self.textEdit.toPlainText()).lower()
        self.n = 0
        self.power = 0
        if self.radio_value == 1:
            alfavit = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        elif self.radio_value == 2:
            alfavit = 'qwertyuiopasdfghjklzxcvbnm'
        elif self.radio_value == 3:
            alfavit = str(self.text_txt)
        self.power = len(alfavit)
        for i in stroka:
            if i in alfavit:
                self.n+=1
        pamyat = self.n*log2(self.power)
        self.textEdit_2.setText(f"Количество символов = {self.n}\n"
                                f"Вес символа = {log2(self.power)} бит\n"
                                f"Объём информации = {str(pamyat)} бит\n")

    def push_button2_func(self):
        self.pushButton_2.clicked.connect(self.open_file_dialog)

