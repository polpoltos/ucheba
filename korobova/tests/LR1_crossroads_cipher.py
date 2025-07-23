def encrypt(message, step):
    first_str, second_str, third_str, result = "", "", "", ""
    temp = 0
    for i in range(len(message)):
        if i % 4 == 0 or i % 4 == 2:
            second_str += message[i]
        if i % 4 == 1:
            first_str += message[i]
        if i % 4 == 3:
            third_str += message[i]

    if len(first_str) % step*3 > 0:
        first_str += " " * (len(first_str) % step * 3)
    if len(second_str) % step * 3 > 0:
        second_str += " " * (len(second_str) % step * 3)
    if len(third_str) % step * 3 > 0:
        third_str += " " * (len(third_str) % step * 3)
        
    print(first_str)
    print(second_str)
    print(third_str)
    
    while len(first_str) + len(second_str) + len(third_str) > 0:
        if temp == 0:
            result += first_str[:step]
            first_str = first_str[step:]

            result += second_str[:step * 2]
            second_str = second_str[step * 2:]

            result += third_str[:step]
            third_str = third_str[step:]
            temp = 1
        if temp == 1:
            result += first_str[:step * 2]
            first_str = first_str[step * 2:]

            result += second_str[:step]
            second_str = second_str[step:]

            result += third_str[:step * 2]
            third_str = third_str[step * 2:]
            temp = 0
    return result
    

def decrypt(encrypted_message, step):
    first_str_dc, second_str_dc,  third_str_dc, result = "", "", "", ""
    temp = 0
    while len(encrypted_message) > 0:
        if temp == 0:
            first_str_dc += encrypted_message[:step]
            encrypted_message = encrypted_message[step:]

            second_str_dc += encrypted_message[:step * 2]
            encrypted_message = encrypted_message[step * 2:]

            third_str_dc += encrypted_message[:step]
            encrypted_message = encrypted_message[step:]
            temp = 1
        if temp == 1:
            first_str_dc += encrypted_message[:step * 2]
            encrypted_message = encrypted_message[step * 2:]

            second_str_dc += encrypted_message[:step]
            encrypted_message = encrypted_message[step:]

            third_str_dc += encrypted_message[:step * 2]
            encrypted_message = encrypted_message[step * 2:]
            temp = 0
    print(first_str_dc)
    print(second_str_dc)
    print(third_str_dc)

    result = ""
    for i in range(len(message)):
        if i % 4 == 0 or i % 4 == 2:
            result += second_str_dc[:1]
            second_str_dc = second_str_dc[1:]
        if i % 4 == 1:
            result += first_str_dc[:1]
            first_str_dc = first_str_dc[1:]
        if i % 4 == 3:
            result += third_str_dc[:1]
            third_str_dc = third_str_dc[1:]
    return result

message = input('Введите исходное сообщение: ')
step = int(input('Введите шаг: '))
encrypted_message = encrypt(message, step)
print(f"Зашифрованное сообщение: {encrypted_message}")

decrypted_message = decrypt(encrypted_message, step)
print(f"Дешифрованное сообщение: {decrypted_message}")
