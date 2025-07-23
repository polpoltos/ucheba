
adfgx_matrix = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]
adfgx_labels = "ADFGX"

# Словарь подстановок
substitution_dict_adfgx = {adfgx_matrix[i][j]: adfgx_labels[i] + adfgx_labels[j] for i in range(5) for j in range(5)}

def adfgx_substitute(text):
#Подстановка
    return ''.join(substitution_dict_adfgx[char] for char in text.upper().replace('J', 'I') if char in substitution_dict_adfgx)

def adfgx_transpose(ciphertext, keyword):
#Перестановка
    cols = len(keyword)
    rows = (len(ciphertext) + cols - 1) // cols
    table = ['' for _ in range(cols)]
    sorted_key_indices = sorted(range(len(keyword)), key=lambda k: keyword[k])

    for i in range(len(ciphertext)):
        col = i % cols
        table[col] += ciphertext[i]

    transposed_text = ''.join(table[i] for i in sorted_key_indices)
    return table, transposed_text

def adfgx_encrypt(text, keyword):
#Шифр
    substituted_text = adfgx_substitute(text)
    table, transposed_text = adfgx_transpose(substituted_text, keyword)
    return substituted_text, table, transposed_text

def adfgx_decrypt(transposed_text, keyword):
#Дешифр
    cols = len(keyword)
    rows = (len(transposed_text) + cols - 1) // cols
    sorted_key_indices = sorted(range(len(keyword)), key=lambda k: keyword[k])

    table = ['' for _ in range(cols)]
    index = 0
    for col in sorted_key_indices:
        table[col] = transposed_text[index:index + rows]
        index += rows

    substituted_text = ''.join(table[col][row] for row in range(rows) for col in range(cols) if row < len(table[col]))

    reverse_substitution_dict = {v: k for k, v in substitution_dict_adfgx.items()}
    decrypted_text = ''.join(reverse_substitution_dict[substituted_text[i:i+2]] for i in range(0, len(substituted_text), 2))
    return table, decrypted_text

# Пример использования шифра ADFGX
input_text = "HELLOO"
keyword_adfgx = "SECRET"
substituted_text, table_adfgx, encrypted_adfgx = adfgx_encrypt(input_text, keyword_adfgx)
table_dec_adfgx, decrypted_adfgx = adfgx_decrypt(encrypted_adfgx, keyword_adfgx)

print("\nADFGX Cipher:")
print("Original Text:", input_text)
print("Substituted Text:", substituted_text)
print("Encryption Table:", table_adfgx)
print("Encrypted Text:", encrypted_adfgx)
print("Decryption Table:", table_dec_adfgx)
print("Decrypted Text:", decrypted_adfgx)
