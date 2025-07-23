S_BOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
]

def circular_left_shift(val, n):
    return ((val << n) & 0xFFFFFFFF) | (val >> (32 - n))

def s_box_transformation(value):
    result = 0
    for i in range(8):
        segment = (value >> (4 * i)) & 0xF
        substituted = S_BOX[i][segment]
        result |= (substituted << (4 * i))
    return result

def gost_round(left, right, key):
    temp = (left + key) % (2 ** 32)
    temp = s_box_transformation(temp)
    temp = circular_left_shift(temp, 11)
    new_left = right ^ temp
    return new_left

def gost_encrypt_block(block, key):
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for i in range(32):
        key_index = i % 8
        left, right = gost_round(left, right, key[key_index]), left
    encrypted_block = (right << 32) | left
    return encrypted_block

def gost_decrypt_block(block, key):
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for i in range(32):
        key_index = (31 - i) % 8
        left, right = gost_round(left, right, key[key_index]), left
    decrypted_block = (right << 32) | left
    return decrypted_block

if __name__ == "__main__":
    key = [
        0x13345779, 0x9BBCDFF1, 0x01234567, 0x89ABCDEF,
        0xFEDCBA98, 0x76543210, 0xF0E1D2C3, 0xB4A59687
    ]

    plaintext_block = 0x1A2F3456BCE78923

    encrypted_block = gost_encrypt_block(plaintext_block, key)
    print(f"Зашифрованный блок: {encrypted_block:016X}")

    decrypted_block = gost_decrypt_block(encrypted_block, key)
    print(f"Расшифрованный блок: {decrypted_block:016X}")

    assert decrypted_block == plaintext_block, "Ошибка: расшифрование не соответствует исходному тексту!"
