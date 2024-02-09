inp_str = input().encode('cp1251').split()
hash_table = [[0]*2 for i in range(8)]


def H(i):
#----------------------------------
    # mod = i * 0.618033 #метод умножения
    # result = int(16 * (mod - int(mod)))
    # print(i, result)
    # return result
#------------------------------------------
    return (int(i)//2) % 8 #метод деления
#-------------------------------------------
    # key = str(i**2) #метод середины квадрата
    # print(i, key[2:3])
    # return int(key[int(len(key)/2):int(len(key)/2 + 1)])
#--------------------------------------------------------
    # result = 0 #Аддитивный метод
    # for j in str(i):
    #     result += int(j)
    # return result % 128


def add(id, dat, type, chain):
    symbol_table[id][0] = id+1
    symbol_table[id][1] = dat # Значение после хеш-функции
    symbol_table[id][2] = type
    symbol_table[id][3] = chain # ссылка друг друга
    return id+1

count = 0
for i in hash_table:
    i[0] = count # номер
    i[1] = 0 # хеш-таблица
    count += 1

symbol_table = []
count = 0

for i in inp_str:
    # print(i, H(i))
    res = H(i) #результат хеш-функции
    if hash_table[res][1] == 0: #проверка на наличие id в хеш-таблицы
        symbol_table.append([0] * 4) #добавление в символьную таблицу строки
        count = add(count, i, "int", 0) #заполнение этой строки
        hash_table[res][1] = count #добавление в хеш-таблицу номера строки


    else:
        id = hash_table[res][1] - 1
        f = True
        if symbol_table[id][1] == i:
            f = False
        while f:
            if symbol_table[id][1] == i:
                 f = False

            else:
                if symbol_table[id][3] == 0:
                    symbol_table[id][3] = count + 1
                    symbol_table.append([0] * 4)
                    count = add(count, i, "int", 0)
                    f = False
                else:
                    id = symbol_table[id][3] - 1


print("Symbol table")
for j in symbol_table:
    print(j)

print("Hash table")
for j in hash_table:
    print(j)

