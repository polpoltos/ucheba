import sys
import time
import threading
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QInputDialog, QColorDialog, QProgressBar, QLineEdit, QMessageBox
import math
from PyQt5.QtCore import Qt


class SubWindowInstruction(QWidget):
    def __init__(self):
        super(SubWindowInstruction, self).__init__()
        self.resize(620, 540)
        self.setWindowTitle('Инструкция')
        self.setStyleSheet('background: rgb(98, 98, 98);')

        # Label
        self.labelTitle = QLabel(self)
        self.labelTitle.setText("\tРуководство по использованию:")
        self.labelTitle.move(10, 0)
        self.labelTitle.setStyleSheet("QLabel{font-size: 14pt;}")

        self.labelInstr = QLabel(self)
        self.labelInstr.move(10, 30)
        self.labelInstr.setText("Загрузите входные данные:\n"
                                "\tнажатием кнопки «Загрузить входные данные»\n"
                                "Запишите результат в файл:\n"
                                "\tнажатием кнопки «Сохранить результат»\n"
                                "\tСписок доступных команд:\n"
                                " esc - выход из программы.\n"
                                "Пожалуйста, проверяйте правильность записи команды!")
        self.labelInstr.setStyleSheet("QLabel{font-size: 10pt;}")



class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,200,600,600)
        self.setWindowTitle("интерфейс")
        self.buttonInsruc = QPushButton("Инструкция", self)
        self.sub_window_instr = SubWindowInstruction()  # новое окно

        # окошко инструкция
        self.buttonInsruc.move(0,520)
        self.buttonInsruc.resize(180,80)
        self.buttonInsruc.setStyleSheet("background: rgb(0,105,105)")
        self.buttonInsruc.clicked.connect(self.sub_window_instr.show)


        self.btInputData = QPushButton("Загрузить входные данные", self)
        self.btInputData.move(50, 10)
        self.btInputData.setStyleSheet("background: rgb(0,255,0)")
        self.btInputData.resize(180, 50)
        self.btInputData.clicked.connect(self.data_entry_dialog)
        # self.btInputData.clicked.connect(self.input_data)



        self.Downloaddata = QPushButton("Сохранить данные",self)
        self.Downloaddata.move(50,145)
        self.Downloaddata.resize(180,50)
        self.Downloaddata.setStyleSheet("background: rgb(0,255,0)")
        self.Downloaddata.clicked.connect(self.Download)




        # окошко с необработанными данными
        self.noConvertedData = QLabel("Необработанные данные", self)
        self.noConvertedData.move(50,150)
        self.noConvertedData.resize(250,250)
        self.noConvertedDataEdit = QLineEdit(self)
        self.noConvertedDataEdit.move(50,290)
        self.noConvertedDataEdit.resize(200, 50)


        self.ExidWindow = QLineEdit(self)
        self.ExidWindow.move(400, 400)
        self.ExidWindow.resize(150,50)

        self.btComandMode = QPushButton("Отправить команду", self)
        self.btComandMode.move(400, 460)
        self.btComandMode.resize(150, 50)
        self.comand = self.ExidWindow.text().split()
        self.btComandMode.clicked.connect(self.comand_mode)





        # окошко с обработанными данными
        self.file = open("test.txt", "w")
        # self.file.close()

        self.ConvertedData = QLabel("Обработанные данные", self)
        self.ConvertedData.move(50,250)
        self.ConvertedData.resize(250,250)
        self.ConvertedDataEdit = QLineEdit(self)
        self.ConvertedDataEdit.move(50,400)
        self.ConvertedDataEdit.resize(300, 50)

    def comand_mode(self):
        if self.comand[0] == 'esc':
            sys.exit()



    def Download(self):
        self.file.write(data + '\n')
        self.file.close()
        self.convert("test.txt")

    def data_entry_dialog(self):
        data, done = QInputDialog.getText(self, "Обработка данных", "Введите строку: ")
        if done:
            self.noConvertedDataEdit.setText(data)
            # self.Download()
            self.file.write(data + '\n')
            self.file.close()
            self.convert("test.txt")








    # загрузка данных
    def input_data(self):
        data, done = QInputDialog.getText(self, "Входные данные", "Введите название файла с входными данными: ")
        freslast = open(data, "r") # открывает файл
        work_str = ''.join(freslast.readlines())   # читает файл
        freslast.close()  # закрыть
        print(work_str.split()) #выводим

    def operator(self, word):
        if (word == "if"):
            return "1"
        if (word == ">"):
            return "2"
        if (word == "THEN"):
            return "3"
        if (word == ":="):
            return "4"
        if (word == "+"):
            return "5"
        if (word == "/"):
            return "6"
        if (word == ";"):
            return "7"
        if (word == "*"):
            return "8"
        if (word == "="):
            return "9"
        if (word == "write"):
            return "10"
        if (word == "("):
            return "11"
        if (word == ")"):
            return "12"
        return " "

    def id(self, word):
        if (word == "N"):
            return "1"
        if (word == "M"):
            return "2"
        if (word == "B"):
            return "3"

    def convert(self, file):
        with open(file, 'r', encoding='utf-8') as d:    #'LRling1.txt'
            for CodeLine in d:
                line = ' '
                for word in CodeLine.split():                #split разбивает стороку на подстроки
                    if word.isalpha() and len(word) == 1:    #isalpha() Возвращает флаг, указывающий на то, содержит ли строка только буквы
                        line += '13' + ' ' + self.id(word) + ' '
                    elif word.isdigit():                     #isdigit() Возвращает флаг, указывающий на то, содержит ли строка только цифры.
                        line += '14' + ' ' + word + ' '
                    else:
                        line += self.operator(word) + ' '
                print(line)
                self.ConvertedDataEdit.setText(line)




app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())