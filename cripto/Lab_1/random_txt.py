def rle_encode(data):
    encoding = ''
    i = 0

    while i < len(data):
        count = 1
        while i + 1 < len(data) and (data[i] == data[i+1]):
            i += 1
            count += 1
            if data[i] == '\n':
                print('puk')
        if data[i] == 'w' or data[i] == 'b':
            encoding += str(count) + data[i]
        i += 1

    return encoding

# Чтение файла
with open('1.txt', 'r') as file:
    data = file.read()

# Применение RLE
encoded_data = rle_encode(data)

# Запись закодированных данных в новый файл
with open('encoded_file.txt', 'w') as file:
    file.write(encoded_data)

print(encoded_data)
