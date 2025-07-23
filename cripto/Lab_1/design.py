from PyQt6 import QtWidgets, QtGui
import sys
import os
from time import sleep


def rle_encode(data):
    encoding = ''
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and (data[i] == data[i + 1]):
            i += 1
            count += 1
        if data[i] in 'wb':
            encoding += str(count) + data[i]
        i += 1
    return encoding

def rle_decode(data):
    decode = ''
    count = ''
    char_count = 0
    for char in data:
        # Если символ является числом
        if char.isdigit():
            count += char
        else:
            decode += char * int(count)
            char_count += int(count)
            count = ''
            # Если количество символов достигло 100, добавить символ новой строки
            if char_count >= 100:
                decode+='\n'
                char_count = 0
    return decode

print("Расшифрованные данные успешно записаны в decoded_file.txt")

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button1 = QtWidgets.QPushButton('Шифратор')
        self.button1.clicked.connect(self.load_file)

        self.button2 = QtWidgets.QPushButton('De`шифратор')
        self.button2.clicked.connect(self.draw_image)

        self.button3 = QtWidgets.QPushButton('INFO')
        self.button3.clicked.connect(self.info)

        self.text_field = QtWidgets.QTextEdit()

        self.output_field1 = QtWidgets.QLabel()
        self.output_field2 = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout(self)
        layout1 = QtWidgets.QHBoxLayout(self)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.text_field)

        layout1.addWidget(self.output_field1)
        layout1.addWidget(self.output_field2)

        layout.addLayout(layout1)

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                image = QtGui.QImage(100, 100, QtGui.QImage.Format.Format_RGB32)
                for i, line in enumerate(text.splitlines()):
                    for j, char in enumerate(line):
                        color = QtGui.QColor('white') if char == 'w' else QtGui.QColor('black')
                        image.setPixelColor(j, i, color)
                self.output_field1.setPixmap(QtGui.QPixmap.fromImage(image))
                encode = rle_encode(text)
                with open('2.txt', 'w') as file:
                    file.write(encode)

    def draw_image(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                encode = rle_decode(text)
                with open('3.txt', 'w') as file:
                    file.write(encode)
                with open('3.txt', 'r') as file:
                    text = file.read()
                    image = QtGui.QImage(100, 100, QtGui.QImage.Format.Format_RGB32)
                    for i, line in enumerate(text.splitlines()):
                        for j, char in enumerate(line):
                            color = QtGui.QColor('white') if char == 'w' else QtGui.QColor('black')
                            image.setPixelColor(j, i, color)
                    self.output_field2.setPixmap(QtGui.QPixmap.fromImage(image))

    def info(self):
        file_name_en, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')

        sleep(1)
        file_name_de, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')

        with open(file_name_en, 'r') as file:
            original_data = file.read()

        # Открытие и чтение расшифрованного файла
        with open(file_name_de, 'r') as file:
            decoded_data = file.read()

        original_file_size = len(original_data) - 100
        decoded_file_size = len(decoded_data)
        print(original_file_size)
        print(decoded_file_size)

        print((1 - (decoded_file_size/original_file_size))*100)
        self.text_field.setText(str((1 - (decoded_file_size/original_file_size))*100))


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
