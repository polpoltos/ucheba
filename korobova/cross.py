message = input("Сообщение (ENG): ").lower()
step = int(input("Введите шаг: "))
result = ""
A = ""
B = ""
C = ""

# Распределение символов по группам
for i in range(len(message)):
    if i % 4 == 0 or i % 4 == 2:
        B += message[i]
    if i % 4 == 1:
        A += message[i]
    if i % 4 == 3:
        C += message[i]

# Дополнение строк до кратности для каждого шага
if len(A) % (step * 3) > 0:
    A += " " * (step * 3 - len(A) % (step * 3))
if len(B) % (step * 3) > 0:
    B += " " * (step * 3 - len(B) % (step * 3))
if len(C) % (step * 3) > 0:
    C += " " * (step * 3 - len(C) % (step * 3))

print(f"A: {A}")
print(f"B: {B}")
print(f"C: {C}")

# Процесс кодирования
Tp = 0
encoded_output = ""
while len(A) + len(B) + len(C) > 0:
    if Tp == 0:
        encoded_output += A[:step]
        A = A[step:]

        encoded_output += B[:step * 2]
        B = B[step * 2:]

        encoded_output += C[:step]
        C = C[step:]
        Tp = 1
    else:
        encoded_output += A[:step * 2]
        A = A[step * 2:]

        encoded_output += B[:step]
        B = B[step:]

        encoded_output += C[:step * 2]
        C = C[step * 2:]
        Tp = 0

print(f"Закодировано: {encoded_output}")

# Раскодирование
A2 = ""
B2 = ""
C2 = ""
Tp = 0
while len(encoded_output) > 0:
    if Tp == 0:
        A2 += encoded_output[:step]
        encoded_output = encoded_output[step:]

        B2 += encoded_output[:step * 2]
        encoded_output = encoded_output[step * 2:]

        C2 += encoded_output[:step]
        encoded_output = encoded_output[step:]
        Tp = 1
    else:
        A2 += encoded_output[:step * 2]
        encoded_output = encoded_output[step * 2:]

        B2 += encoded_output[:step]
        encoded_output = encoded_output[step:]

        C2 += encoded_output[:step * 2]
        encoded_output = encoded_output[step * 2:]
        Tp = 0

print(f"A2: {A2}")
print(f"B2: {B2}")
print(f"C2: {C2}")

# Финальное восстановление исходного сообщения
decoded_output = ""
for i in range(len(message)):
    if i % 4 == 0 or i % 4 == 2:
        decoded_output += B2[:1]
        B2 = B2[1:]
    if i % 4 == 1:
        decoded_output += A2[:1]
        A2 = A2[1:]
    if i % 4 == 3:
        decoded_output += C2[:1]
        C2 = C2[1:]

print(f"Раскодировано: {decoded_output}")
