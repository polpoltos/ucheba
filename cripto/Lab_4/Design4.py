import collections
from PyQt6 import QtWidgets
import sys


def arithmetic_coding(message):
    freq = collections.Counter(message)
    total = len(message)
    prob = {char: count/total for char, count in freq.items()}
    intervals = {}
    lower_bound = 0
    for char, p in prob.items():
        intervals[char] = (lower_bound, lower_bound + p)
        lower_bound += p
    lower, upper = 0, 1
    for char in message:
        l, u = intervals[char]
        lower, upper = lower + (upper - lower)*l, lower + (upper - lower)*u
    return (lower + upper) / 2, freq

def arithmetic_decoding(number, freq, length):
    prob = {char: count/length for char, count in freq.items()}
    intervals = {}
    lower_bound = 0
    for char, p in prob.items():
        intervals[char] = (lower_bound, lower_bound + p)
        lower_bound += p
    message = ''
    for _ in range(length):
        for char, (l, u) in intervals.items():
            if l <= number < u:
                message += char
                number = (number - l) / (u - l)
                break
    return message


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button1 = QtWidgets.QPushButton('Кодирование')
        self.button1.clicked.connect(self.load_file)

        self.button2 = QtWidgets.QPushButton('Декодирование')
        self.button2.clicked.connect(self.draw_image)


        self.text_field = QtWidgets.QTextEdit()

        self.output_field1 = QtWidgets.QLabel()
        self.output_field2 = QtWidgets.QLabel()
        self.lenght = 0
        self.freq_0 = 0

        layout = QtWidgets.QVBoxLayout(self)
        layout1 = QtWidgets.QHBoxLayout(self)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.text_field)

        layout1.addWidget(self.output_field1)
        layout1.addWidget(self.output_field2)

        layout.addLayout(layout1)

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if file_name:
            with open(file_name, 'r') as file:
                message = file.read()
                self.lenght = len(message)
                number, freq = arithmetic_coding(message)
                self.freq_0 = freq
                self.text_field.setText(str(freq))
                with open('2.txt', 'w') as f:
                    f.write(str(number))
                with open('code.txt', 'w') as f:
                    f.write(str(freq))


    def draw_image(self):
        with open('code.txt', 'r') as file:
            freq = file.read()
        with open('2.txt', 'r') as f0:
            number = f0.read()
            decoded_message = arithmetic_decoding(float(number), self.freq_0, self.lenght)
        with open('3.txt', 'w') as f:
            f.write(decoded_message)


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

