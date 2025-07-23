def create_substitution_table(key):
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"
    table = {}
    key_used = []

    # Создаем таблицу замены, используя ключевое слово
    for char in key.upper():
        if char not in key_used and char in alphabet:
            table[char] = None
            key_used.append(char)

    # Заполняем таблицу оставшимися буквами алфавита
    for char in alphabet:
        if char not in key_used:
            key_used.append(char)

    # Создаем пару (буква алфавита, буква замены) в таблице
    for i in range(len(alphabet)):
        table[alphabet[i]] = key_used[i]

    return table

def encrypt(message, key):
    table = create_substitution_table(key)
    print(table)
    encrypted_message = ''

    for char in message.upper():
        if char in table:
            encrypted_message += table[char]
        else:
            encrypted_message += char  # не шифруем пробелы и знаки

    return encrypted_message

def decrypt(encrypted_message, key):
    table = create_substitution_table(key)
    reversed_table = {v: k for k, v in table.items()}
    decrypted_message = ''

    for char in encrypted_message.upper():
        if char in reversed_table:
            decrypted_message += reversed_table[char]
        else:
            decrypted_message += char  # не расшифровываем пробелы и знаки

    return decrypted_message

# Пример использования
key = "ключ"
message = 'Лига КВН'

encrypted = encrypt(message, key)
decrypted = decrypt(encrypted, key)

print(f'Original Message: {message}')
print(f'Encrypted Message: {encrypted}')
print(f'Decrypted Message: {decrypted}')
