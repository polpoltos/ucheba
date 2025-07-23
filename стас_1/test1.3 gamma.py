alphabet = {"А": 1, "Б": 2, "В": 3,
            "Г": 4, "Д": 5, "Е": 6, "Ё": 7,
            "Ж": 8, "З": 9, "И": 10, "Й": 11,
            "К": 12, "Л": 13, "М": 14, "Н": 15,
            "О": 16, "П": 17, "Р": 18, "С": 19,
            "Т": 20, "У": 21, "Ф": 22, "Х": 23,
            "Ц": 24, "Ч": 25, "Ш": 26, "Щ": 27,
            "Ъ": 28, "Ы": 29, "Ь": 30, "Э": 31,
            "Ю": 32, "Я": 33, " ": 34}


def encode(message, gamma):
    text_len = len(message)
    gamma_len = len(gamma)
    code = []
    message = message.upper()
    gamma = gamma.upper()

    key_text = []
    for i in range(text_len // gamma_len):
        for symbol in gamma:
            key_text.append(symbol)

    for i in range(text_len % gamma_len):
        key_text.append(gamma[i])

    print("Зашифровка")
    print(list(message))
    print(key_text)

    for i in range(text_len):
        code.append((alphabet[message[i]] + alphabet[key_text[i]]) % 34)

    print(code)

    encode_text = []
    for i in range(len(code)):
        key = next(key for key, value in alphabet.items() if value == code[i])
        encode_text.append(key)

    print(encode_text)

    return "".join(encode_text)


def decode(code, gamma):
    code_len = len(code)
    gamma_len = len(gamma)
    decode = []
    code = code.upper()
    gamma = gamma.upper()

    key_text = []
    for i in range(code_len // gamma_len):
        for symbol in gamma:
            key_text.append(symbol)

    for i in range(code_len % gamma_len):
        key_text.append(gamma[i])

    print("\nРасшифровка")
    print(list(code))
    print(key_text)

    for i in range(code_len):
        decode.append(((alphabet[code[i]] - alphabet[key_text[i]]) + 34) % 34)

    print(decode)

    decode_text = []
    for i in range(len(decode)):
        key = next(key for key, value in alphabet.items() if value == decode[i])
        decode_text.append(key)

    print(decode_text)

    return "".join(decode_text)


def main():
    message = input("Введите сообщение на русском языке (можно использовать пробелы): ")
    gamma = input("Введите ключ: ")
    encoded_message = encode(message, gamma)
    decoded_message = decode(encoded_message, gamma)

    print("\n")
    print(f"Исходное сообщение: {message.upper()}; ключ: {gamma.upper()}")
    print(f"Закодированное сообщение: {encoded_message}")
    print(f"Раскодированное сообщение: {decoded_message}")


if __name__ == '__main__':
    main()
