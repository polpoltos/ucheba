def generate_binary_gamma(length):
    """Генерация двоичной гаммы заданной длины."""
    from random import choice
    return ''.join(choice(['0', '1']) for _ in range(length))

def binary_mod2_encrypt(text, gamma):
    """Шифрование гаммированием по модулю 2 (битовое XOR)."""
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    encrypted_binary = ''.join(str(int(bt) ^ int(g)) for bt, g in zip(binary_text, gamma))

    return binary_text, encrypted_binary

def binary_mod2_decrypt(encrypted_binary, gamma):
    """Дешифрование гаммированием по модулю 2 (битовое XOR)."""
    decrypted_binary = ''.join(str(int(eb) ^ int(g)) for eb, g in zip(encrypted_binary, gamma))

    # Преобразование обратно в текст
    decrypted_text = ''.join(chr(int(decrypted_binary[i:i+8], 2)) for i in range(0, len(decrypted_binary), 8))
    return decrypted_binary, decrypted_text

# Пример использования гаммирования по модулю 2
input_text = "HELLO"
gamma = generate_binary_gamma(len(input_text) * 8)

binary_text, encrypted_binary = binary_mod2_encrypt(input_text, gamma)
decrypted_binary, decrypted_text = binary_mod2_decrypt(encrypted_binary, gamma)

print("Гаммирование по модулю 2 (битовый XOR):")
print("Original Binary:", binary_text)
print("Gamma:", gamma)
print("Encrypted Binary:", encrypted_binary)
print("Decrypted Binary:", decrypted_binary)
print("Decrypted Text:", decrypted_text)
