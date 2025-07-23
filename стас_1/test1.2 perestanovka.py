def permute_block(block, key):
    return ''.join([block[i - 1] for i in key])


def encode_message(message, key):
    block_size = len(key)
    encoded_message = ""

    for i in range(0, len(message), block_size):
        block = message[i:i + block_size]
        # print(block)
        if len(block) < block_size:
            block += " " * (block_size - len(block))

        encoded_message += permute_block(block, key)
    return encoded_message


def decode_message(encoded_message, key):
    block_size = len(key)
    decoded_message = ""

    inverse_key = [0] * block_size
    for i, pos in enumerate(key):
        inverse_key[pos - 1] = i + 1

    for i in range(0, len(encoded_message), block_size):
        block = encoded_message[i:i + block_size]
        print(block)
        decoded_message += permute_block(block, inverse_key)

    return decoded_message.strip()


def main():
    message = input('Введите сообщение: ')
    # key = input('Введите ключ в виде последовательности чисел без пробелов и запятых: ')
    key = [1, 3, 4, 2]
    keys = [int(item) for item in key]
    encoded = encode_message(message.upper(), keys)
    decoded = decode_message(encoded, keys)

    print(f"Исходное сообщение: {message.upper()}")
    print(f"Закодированное сообщение: {encoded}")
    print(f"Декодированное сообщение: {decoded}")


if __name__ == '__main__':
    main()
