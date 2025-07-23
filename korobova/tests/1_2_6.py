def columnar_transposition_encrypt_with_dimensions(text, rows, cols):
    """Шифрование вертикальной перестановкой с указанием рядов и столбцов."""
    table = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0

    # Заполнение таблицы по строкам
    for r in range(rows):
        for c in range(cols):
            if index < len(text):
                table[r][c] = text[index]
                index += 1

    # Выписывание текста по столбцам
    encrypted_text = ''.join(table[r][c] for c in range(cols) for r in range(rows) if table[r][c])

    return table, encrypted_text

def columnar_transposition_decrypt_with_dimensions(encrypted_text, rows, cols):
    """Дешифрование вертикальной перестановкой с указанием рядов и столбцов."""
    table = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0

    # Заполнение таблицы по столбцам
    for c in range(cols):
        for r in range(rows):
            if index < len(encrypted_text):
                table[r][c] = encrypted_text[index]
                index += 1

    # Выписывание текста по строкам
    decrypted_text = ''.join(table[r][c] for r in range(rows) for c in range(cols) if table[r][c])

    return table, decrypted_text

# Пример использования Вертикальной перестановки с указанными размерами
input_text = "Helloworld"
rows, cols = 2, 5
table, encrypted_columnar = columnar_transposition_encrypt_with_dimensions(input_text, rows, cols)
table_dec, decrypted_columnar = columnar_transposition_decrypt_with_dimensions(encrypted_columnar, rows, cols)

print("\nColumnar Transposition (Dimensions):")
print("Original:", input_text)
print("Table (Encryption):", table)
print("Encrypted:", encrypted_columnar)
print("Table (Decryption):", table_dec)
print("Decrypted:", decrypted_columnar)
