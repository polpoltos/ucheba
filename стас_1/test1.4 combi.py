import math
import random


def encode(message, key, polybius):
    message = message.upper()
    key = key.upper()
    temp = ""
    adfgvx = "ADFGVX"
    for ch in message:
        for i in range(6):
            for j in range(6):
                if polybius[i][j] == ch:
                    temp += adfgvx[i] + adfgvx[j]
    print(temp)

    num_cols = len(key)
    num_rows = math.ceil(len(temp) / num_cols)
    table = [["" for _ in range(num_cols)] for _ in range(num_rows)]

    index = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if index < len(temp):
                table[i][j] = temp[index]
                index += 1
    print(table)

    sorted_key = sorted(list(enumerate(key)), key=lambda x: x[1])
    print(sorted_key)
    permuted_cols = [""] * num_cols
    for i, (original_index, _) in enumerate(sorted_key):
        permuted_cols[i] = "".join([row[original_index] for row in table])

    print(permuted_cols)
    return permuted_cols


def decode(encoded_message, key, polybius):
    print("\nДекодирование")
    key = key.upper()
    col_strs = encoded_message
    max_col_len = max(len(s) for s in col_strs)
    cols = [list(s) for s in col_strs]
    for i in range(len(cols)):
        if len(cols[i]) < max_col_len:
            cols[i].extend([''] * (max_col_len - len(cols[i])))

    print(cols)

    table = [['' for _ in range(len(key))] for _ in range(max_col_len)]
    order = orderKey(key)
    for i in range(max_col_len):
        for j in range(len(key)):
            table[i][order[j]] = cols[j][i]

    print(table)

    temp = ""
    for row in table:
        temp += "".join(row)

    plainText = ""
    adfgvx = "ADFGVX"
    for i in range(0, len(temp), 2):
        r = adfgvx.index(temp[i])
        c = adfgvx.index(temp[i + 1])
        plainText += polybius[r][c]

    return plainText


def orderKey(key):
    temp = [(key[i], i) for i in range(len(key))]
    temp.sort(key=lambda x: x[0])
    res = [x[1] for x in temp]
    return res


def main():
    message = input("Введите сообщение на русском языке: ")
    key = input("Введите ключ: ")
    labels = ['A', 'D', 'F', 'G', 'V', 'X']
    polybius = [["\0" for _ in range(6)] for _ in range(6)]
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ---"
    words = list(alphabet)
    random.shuffle(words)
    print(words)

    for i in range(6):
        for j in range(6):
            polybius[i][j] = words[6 * i + j]

    print("    ", " ".join(labels))
    print("-----------------")
    for i, row in enumerate(polybius):
        print(labels[i], "| ", " ".join(row))

    encoded_message = encode(message, key, polybius)
    decoded_message = decode(encoded_message, key, polybius)

    print(f"Исходное сообщение: {message.upper()}; ключ: {key.upper()}")
    print(f"Закодированное сообщение: {" ".join(encoded_message)}")
    print(f"Раскодированное сообщение: {decoded_message}")


if __name__ == '__main__':
    main()
