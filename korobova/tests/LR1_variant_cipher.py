def generate_cipher_grid(secret):
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЪЭЮЯ"
    unique_key = "".join(dict.fromkeys(secret))  # Сохраняем порядок символов без дубликатов
    cipher_grid = []

    for ch in unique_key:
        if ch in letters:
            letters = letters.replace(ch, "")
            cipher_grid.append(ch)

    cipher_grid.extend(letters)
    return cipher_grid


def build_coordinate_map(grid):
    coord_map = {}
    idx = 0
    for ch in grid:
        row_pos = idx // 6
        col_pos = idx % 6
        coord_map[ch] = (row_pos, col_pos)
        idx += 1
    return coord_map


def encode_message(text, secret):
    grid = generate_cipher_grid(secret)
    coord_map = build_coordinate_map(grid)
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЪЭЮЯ"
    row_ids = letters[:6]
    col_ids = letters[6:12]

    encoded_text = ""
    for symbol in text:
        if symbol in coord_map:
            row, col = coord_map[symbol]
            encoded_text += row_ids[row] + col_ids[col]
    print(encoded_text)
    return encoded_text


def decode_message(coded_text, secret):
    grid = generate_cipher_grid(secret)
    coord_map = build_coordinate_map(grid)
    letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЪЭЮЯ"
    row_ids = letters[:6]
    col_ids = letters[6:12]

    decoded_text = ""
    for i in range(0, len(coded_text), 2):
        row_symbol = coded_text[i]
        col_symbol = coded_text[i + 1]

        row = row_ids.index(row_symbol)
        col = col_ids.index(col_symbol)

        decoded_text += grid[row * 6 + col]

    return decoded_text


def display_cipher_grid(grid):
    for i in range(0, len(grid), 6):
        row = grid[i:i + 6]
        print(" ".join(row))


# Пример работы
user_key = input('Введите ключ: ').upper()
user_message = input('Введите сообщение: ').upper()

print("Шифровальная таблица:")
cipher_grid = generate_cipher_grid(user_key)
display_cipher_grid(cipher_grid)

encoded_text = encode_message(user_message, user_key)
print(f"Зашифрованный текст: {encoded_text}")
decoded_text = decode_message(encoded_text, user_key)
print(f"Расшифрованный текст: {decoded_text}")
