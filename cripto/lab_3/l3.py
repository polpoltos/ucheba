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


if __name__ == "__main__":
    # Чтение файла 1.txt и подсчет частот символов
    with open("1.txt", "r") as file:
        message = file.read()

    frequencies = defaultdict(int)
    for char in message:
        frequencies[char] += 1

    # Построение дерева Хаффмана
    huffman_tree_root = build_huffman_tree(frequencies)

    # Создание кодов Хаффмана
    huffman_codes = {}
    generate_huffman_codes(huffman_tree_root, "", huffman_codes)

    # Запись таблицы частот и кодов в файл
    with open("huffman_codes.txt", "w") as code_file:
        for char, code in huffman_codes.items():
            freq = frequencies[char]
            code_file.write(f"Символ: {char}, Частота: {freq}, Код: {code}\n")

    # Сжатие сообщения
    compressed_bits = compress_message(message, huffman_codes)
    with open("2.txt", "w") as file:
        file.write(compressed_bits)

    # Декомпрессия
    decompressed_message = decompress_bits(compressed_bits, huffman_tree_root)
    with open("3.txt", "w") as file:
        file.write(decompressed_message)

