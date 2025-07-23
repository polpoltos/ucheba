def create_random_binary_key(size):
    """Создает случайный двоичный ключ указанной длины."""
    import random
    return ''.join(random.choice(['0', '1']) for _ in range(size))

def xor_encrypt(text, key):
    """Шифрует текст с помощью гаммирования по XOR."""
    text_in_binary = ''.join(format(ord(symbol), '08b') for symbol in text)  # Преобразуем текст в двоичный вид
    encrypted_result = ''.join(str(int(b) ^ int(k)) for b, k in zip(text_in_binary, key))  # XOR для каждого бита

    return text_in_binary, encrypted_result

def xor_decrypt(encrypted_binary, key):
    """Расшифровка текста с использованием гаммирования по XOR."""
    decrypted_binary = ''.join(str(int(e) ^ int(k)) for e, k in zip(encrypted_binary, key))

    # Преобразуем двоичный код обратно в текст
    decoded_text = ''.join(chr(int(decrypted_binary[i:i+8], 2)) for i in range(0, len(decrypted_binary), 8))
    return decrypted_binary, decoded_text

# Пример работы с гаммированием XOR
original_text = "HELLO"
key = create_random_binary_key(len(original_text) * 8)

# Шифрование
binary_representation, encrypted_output = xor_encrypt(original_text, key)

# Дешифрование
decrypted_binary_repr, final_text = xor_decrypt(encrypted_output, key)

print("Гаммирование 2:")
print("Исходный текст в двоичном виде:", binary_representation)
print("Случайный ключ:", key)
print("Зашифрованный текст в двоичном виде:", encrypted_output)
print("Расшифрованный двоичный код:", decrypted_binary_repr)
print("Расшифрованный текст:", final_text)
