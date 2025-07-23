# Матрица для ADFGX-шифра
cipher_grid = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]
grid_labels = "ADFGX"

# Создание словаря замен на основе матрицы
substitution_map = {cipher_grid[i][j]: grid_labels[i] + grid_labels[j] for i in range(5) for j in range(5)}

def substitute_adfgx(message):
    """Функция замены символов по ADFGX."""
    return ''.join(substitution_map[char] for char in message.upper().replace('J', 'I') if char in substitution_map)

def transpose_adfgx(encoded_text, key):
    """Перестановка текста по ключу."""
    col_count = len(key)
    row_count = (len(encoded_text) + col_count - 1) // col_count
    transposition_table = ['' for _ in range(col_count)]
    ordered_key_indices = sorted(range(len(key)), key=lambda idx: key[idx])

    for idx, char in enumerate(encoded_text):
        column = idx % col_count
        transposition_table[column] += char

    encrypted_output = ''.join(transposition_table[i] for i in ordered_key_indices)
    return transposition_table, encrypted_output

def adfgx_encrypt(message, key):
    """Основная функция шифрования ADFGX."""
    encoded_message = substitute_adfgx(message)
    table, encrypted_message = transpose_adfgx(encoded_message, key)
    return encoded_message, table, encrypted_message

def adfgx_decrypt(encrypted_message, key):
    """Функция дешифрования ADFGX."""
    col_count = len(key)
    row_count = (len(encrypted_message) + col_count - 1) // col_count
    ordered_key_indices = sorted(range(len(key)), key=lambda idx: key[idx])

    transposition_table = ['' for _ in range(col_count)]
    current_index = 0
    for col in ordered_key_indices:
        transposition_table[col] = encrypted_message[current_index:current_index + row_count]
        current_index += row_count

    decoded_sequence = ''.join(
        transposition_table[col][row] for row in range(row_count) for col in range(col_count) if row < len(transposition_table[col])
    )

    # Обратная подстановка символов
    reverse_map = {v: k for k, v in substitution_map.items()}
    decrypted_message = ''.join(reverse_map[decoded_sequence[i:i+2]] for i in range(0, len(decoded_sequence), 2))
    return transposition_table, decrypted_message

# Пример работы шифра ADFGX
sample_text = "KVN LIGA"
key_for_adfgx = "KEY"
encoded_seq, transposition_table, encrypted_text = adfgx_encrypt(sample_text, key_for_adfgx)
decryption_table, decrypted_text = adfgx_decrypt(encrypted_text, key_for_adfgx)

print("\nADFGX Cipher:")
print("Исходный текст:", sample_text)
print("Закодированный текст:", encoded_seq)
print("Таблица перестановки:", transposition_table)
print("Шифротекст:", encrypted_text)
print("Таблица дешифрования:", decryption_table)
print("Расшифрованный текст:", decrypted_text)
