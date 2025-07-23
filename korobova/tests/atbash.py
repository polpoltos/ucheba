def atbash_cipher_ru(text):
    russian_alphabet = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
    reversed_alphabet = russian_alphabet[::-1]
    translation_table = str.maketrans(russian_alphabet, reversed_alphabet)
    return text.upper().translate(translation_table)

# Пример использования Атбаш для русского текста
input_text = str(input('Original: '))
encrypted_atbash = atbash_cipher_ru(input_text)
decrypted_atbash = atbash_cipher_ru(encrypted_atbash)

print("Encrypted:", encrypted_atbash)
print("Decrypted:", decrypted_atbash)
