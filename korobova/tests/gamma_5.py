import random

# Создаем алфавит из русских букв и пробела
russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ "
alphabet_size = len(russian_alphabet)  # Это будет модуль N, равный 34

# Создаем словари для сопоставления символов с номерами и обратно
char_to_num = {char: i for i, char in enumerate(russian_alphabet)}
num_to_char = {i: char for i, char in enumerate(russian_alphabet)}

def generate_gamma(length):
    """Генерация гаммы для русского алфавита с учетом пробела."""
    return [random.randint(0, alphabet_size - 1) for _ in range(length)]

def mod_n_encrypt_russian(text, gamma):
    """Шифрование гаммированием по модулю N для русского алфавита."""
    # Преобразуем текст в номера символов
    text_nums = [char_to_num[char] for char in text]
    # Шифрование по модулю N
    encrypted_nums = [(text_num + gamma[i]) % alphabet_size for i, text_num in enumerate(text_nums)]
    encrypted_text = ''.join(num_to_char[num] for num in encrypted_nums)

    return text_nums, encrypted_nums, encrypted_text

def mod_n_decrypt_russian(encrypted_nums, gamma):
    """Дешифрование гаммированием по модулю N для русского алфавита."""
    # Дешифрование по модулю N
    decrypted_nums = [(encrypted_num - gamma[i]) % alphabet_size for i, encrypted_num in enumerate(encrypted_nums)]
    decrypted_text = ''.join(num_to_char[num] for num in decrypted_nums)

    return decrypted_nums, decrypted_text

# Пример использования гаммирования по модулю N для русского алфавита
input_text = "ПРИВЕТ МИР"
# gamma = generate_gamma(len(input_text))
gamma = generate_gamma(14)
# Шифрование
text_nums, encrypted_nums, encrypted_text = mod_n_encrypt_russian(input_text, gamma)
# Дешифрование
decrypted_nums, decrypted_text = mod_n_decrypt_russian(encrypted_nums, gamma)

print("Гаммирование по модулю N (Русский алфавит):")
print("Original Text:", input_text)
print("Text to Numbers:", text_nums)
print("Gamma:", gamma)
print("Encrypted Numbers:", encrypted_nums)
print("Encrypted Text:", encrypted_text)
print("Decrypted Numbers:", decrypted_nums)
print("Decrypted Text:", decrypted_text)
