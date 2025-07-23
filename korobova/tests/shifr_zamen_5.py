import string


def playfair_key_matrix(keyword):

    keyword = keyword.upper().replace("J", "I")
    matrix = []
    used_letters = set()

    for char in keyword:
        if char not in used_letters and char in string.ascii_uppercase:
            matrix.append(char)
            used_letters.add(char)

    for char in string.ascii_uppercase:
        if char not in used_letters and char != 'J':
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def flatten_matrix(matrix):
    return [char for row in matrix for char in row]


def playfair_encrypt(text, keyword):
    m = playfair_key_matrix(keyword)
    for i in m:
        print(i)
    matrix = flatten_matrix(m)
    text = text.upper().replace("J", "I")

    pairs = []
    i = 0
    while i < len(text):
        char1 = text[i]
        char2 = text[i + 1] if i + 1 < len(text) else 'X'

        if char1 == char2:
            pairs.append((char1, 'X'))
            i += 1
        else:
            pairs.append((char1, char2))
            i += 2

    encrypted_text = ''
    for char1, char2 in pairs:
        row1, col1 = divmod(matrix.index(char1), 5)
        row2, col2 = divmod(matrix.index(char2), 5)

        if row1 == row2:
            encrypted_text += matrix[row1 * 5 + (col1 + 1) % 5] + matrix[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[((row1 + 1) % 5) * 5 + col1] + matrix[((row2 + 1) % 5) * 5 + col2]
        else:
            encrypted_text += matrix[row1 * 5 + col2] + matrix[row2 * 5 + col1]

    return encrypted_text


def playfair_decrypt(ciphertext, keyword):
    matrix = flatten_matrix(playfair_key_matrix(keyword))
    decrypted_text = ''

    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i + 1]
        row1, col1 = divmod(matrix.index(char1), 5)
        row2, col2 = divmod(matrix.index(char2), 5)

        if row1 == row2:
            decrypted_text += matrix[row1 * 5 + (col1 - 1) % 5] + matrix[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += matrix[((row1 - 1) % 5) * 5 + col1] + matrix[((row2 - 1) % 5) * 5 + col2]
        else:
            decrypted_text += matrix[row1 * 5 + col2] + matrix[row2 * 5 + col1]

    return decrypted_text



input_text = "HAIR"
print("Сообщение:", input_text)
playfair_key = "KEYWORD"
encrypted_playfair = playfair_encrypt(input_text, playfair_key)
decrypted_playfair = playfair_decrypt(encrypted_playfair, playfair_key)

print("Щифр:", encrypted_playfair)
print("Дефишр:", decrypted_playfair)
