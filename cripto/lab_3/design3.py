from PyQt6 import QtWidgets, QtGui
import sys
import heapq
from collections import defaultdict


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


def build_huffman_tree(frequencies):
    heap = [[freq, Node(char, freq)] for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        freq1, left_node = heapq.heappop(heap)
        freq2, right_node = heapq.heappop(heap)

        merged_node = Node(None, freq1 + freq2)
        merged_node.left = left_node
        merged_node.right = right_node

        heapq.heappush(heap, [merged_node.freq, merged_node])

    return heap[0][1]


def generate_huffman_codes(root, current_code="", huffman_codes={}):
    if root is None:
        return

    if root.char:
        huffman_codes[root.char] = current_code
        return

    generate_huffman_codes(root.left, current_code + "0", huffman_codes)
    generate_huffman_codes(root.right, current_code + "1", huffman_codes)


def compress_message(message, huffman_codes):
    compressed_bits = "".join(huffman_codes[char] for char in message)
    return compressed_bits


def decompress_bits(compressed_bits, root):
    current_node = root
    decompressed_message = ""

    for bit in compressed_bits:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char:
            decompressed_message += current_node.char
            current_node = root

    return decompressed_message



class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button1 = QtWidgets.QPushButton('Процесс')
        self.button1.clicked.connect(self.load_file)

        self.button2 = QtWidgets.QPushButton('Таблица и коды')
        self.button2.clicked.connect(self.draw_image)


        self.text_field = QtWidgets.QTextEdit()

        self.output_field1 = QtWidgets.QLabel()
        self.output_field2 = QtWidgets.QLabel()

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
                all = len(message)
                frequencies = defaultdict(int)
                for char in message:
                    frequencies[char] += 1
                huffman_tree_root = build_huffman_tree(frequencies)

                huffman_codes = {}
                generate_huffman_codes(huffman_tree_root, "", huffman_codes)
                with open("huffman_codes.txt", "w") as code_file:
                    for char, code in huffman_codes.items():
                        freq = frequencies[char]
                        code_file.write(f"Символ: {char}, Частота: {round(freq/all, 2)}, Код: {code}\n")


                compressed_bits = compress_message(message, huffman_codes)
                with open("2.txt", "w") as file:
                    file.write(compressed_bits)


                decompressed_message = decompress_bits(compressed_bits, huffman_tree_root)
                with open("3.txt", "w") as file:
                    file.write(decompressed_message)

    def draw_image(self):
        with open('huffman_codes.txt', 'r') as file:
            text = file.read()
            self.text_field.setText(text)




app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
