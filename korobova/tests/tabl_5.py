def route_cipher_encrypt(text, rows, cols):

    table = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0

    for r in range(rows):
        for c in range(cols):
            if index < len(text):
                table[r][c] = text[index]
                index += 1


    encrypted_text = ''.join(table[r][c] for c in range(cols) for r in range(rows))

    return table, encrypted_text

def route_cipher_decrypt(encrypted_text, rows, cols):

    table = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0

    for c in range(cols):
        for r in range(rows):
            if index < len(encrypted_text):
                table[r][c] = encrypted_text[index]
                index += 1

    decrypted_text = ''.join(table[r][c] for r in range(rows) for c in range(cols))

    return table, decrypted_text

input_text = "Я люблю криптографику"
print(len(input_text))
rows, cols = 3, 7
table, encrypted_route = route_cipher_encrypt(input_text, rows, cols)
table_dec, decrypted_route = route_cipher_decrypt(encrypted_route, rows, cols)


print("Original:", input_text)
print("Table:")
for i in table:
    print(i)
print("Encrypted:", encrypted_route)
print("Decrypted:", decrypted_route)
