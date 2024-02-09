import sys

config = {
    '1': "if",
    '2': ">",
    '3': "THEN",
    '4': ":=",
    '5': "+",
    '6': "/",
    '7': ";",
    '8': "*",
    '9': "=",
    '10': "write",
    '11': "(",
    '12': ")",
    '13': "ids",
    '14': "const"
}
ids = {
    "1": 'N',
    "2": 'M',
    "3": 'B',
}

freslast = open("code.txt", "r")
work_str = ''.join(freslast.readlines())
freslast.close()
print(work_str.split())
result = []

def list_of_operators(str, result): #<список операторов> -> либо мы находим ;, либо выходим из системы после того, как всё нашли
    for i, value in enumerate(str):
        if (str[int(i)] == '7'): #если мы нашли в итоге ;
            op(str, result)
        if (len(str) == 2): #выход из системы
            result.append(config['7']) #Добавляем в массив то, что осталось
            result.append(config['7'])
            print(result)
            sys.exit()

def op(str, result): #<операторы> -> либо мы находим <УО>, либо <присваивание>, либо <вывод>
    for i, value in enumerate(str):
        if (str[int(i)] == '1' and str[int(i) - 1] != '13') or (str[int(i)] == '3' and str[int(i) - 1] == str[int(i) - 2] == '7'): #<УО>
            CO(str, result) #Если мы нашли <УО>, то переходим в него
        if str[int(i)] == '4' and str[int(i)-2] == '13': #<присваивание>
            assignment(str, result) #Если мы нашли <присваивание>, то переходим в него
        if str[int(i)] == '10': #<вывод>
            conclusion(str, result) #Если мы нашли <вывод>, то переходим в него

def CO(str, result): #<УО> -> тут мы находим if, THEN, <выражение условия>
    j = 0
    for i, value in enumerate(str):
        if str[int(i)] == '1' and str[int(i) - 1] != '13': #тут мы находим if
            j = i + 1
            result.append(config['1']) #Добавляем if в массив
            CO((str[:(i)] + str[j:]), result)#Возвращаемся в <УО>, срезав найденные элементы и ищем оставшееся
        if str[int(i)] == '3' and str[int(i) - 1] != '13': #тут мы находим THEN
            j = i + 1
            result.append(config['3']) #Добавляем THEN в массив
            list_of_operators((str[:(i)] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы
        if (str[int(i)] == '2' or str[int(i)] == '9') and str[int(i) - 2] == '13': #тут мы находим <выражение условия>
            condition_expression(str, result)#Переходим в <выражение условия>

def condition_expression(str, result):#<выражение условия> -> здесь ищем идентификаторы, >, константы
    j = 0
    for i, value in enumerate(str):
        if str[int(i)] == '0' and str[int(i) - 2] == '2':#Здесь мы находим выражение условия для первого <УО>
            j = i + 1
            result.append(ids['1'] + config['2'] + str[i])#Записываем N>0
            list_of_operators((str[:(i) - 4] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы
        if str[int(i)] == '0' and str[int(i) - 2] == '9':#Здесь мы находим выражение условия для первого <УО>,
            j = i + 1
            result.append(ids['3'] + config['9'] + str[i])#Записываем B=0
            list_of_operators((str[:(i) - 4] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы

def assignment(str, result):#<Присваивание> -> здесь ищем идентификаторы, := и <выражение>
    j = 0
    for i, value in enumerate(str):
        if str[int(i)] == '4' and str[int(i) - 2] == '13':#Если мы нашли :=, а перед ним идентификатор
            for i, value in enumerate(str):#Заходим в цикл и ищем конкретный идентификатор
                if str[int(i)] == '4' and str[int(i) - 1] == '2':#Здесь M:=
                    j = i + 1
                    result.append(ids['2'])
                    result.append(config['4'])
                    assignment((str[:(i) - 2] + str[j:]), result)#Возвращаемся в <Присваивание>, срезав найденные элементы и ищем оставшееся
                if str[int(i)] == '4' and str[int(i) - 1] == '3':#Здесь B:=
                    j = i + 1
                    result.append(ids['3'])
                    result.append(config['4'])
                    assignment((str[:(i) - 2] + str[j:]), result)#Возвращаемся в <Присваивание>, срезав найденные элементы и ищем оставшееся
        if str[int(i)] == '5' or str[int(i)] == '6' or str[int(i)] == '8':#Если мы нашли вычисления, то переходим в <выражение>
            expression(str, result)

def expression(str, result):#<Выражение> -> здесь ищем <слагаемые> и +
    j = 0
    for i, value in enumerate(str):
        if str[int(i)] == '5' and str[int(i)-1] != '13':#Если нашли +
            j = i + 1
            result.append(config['5'])#Записываем +
            expression((str[:(i)] + str[j:]), result)#Возвращаемся в <Выражение>, срезав найденные элементы и ищем оставшееся
        if str[int(i)] == '3' and str[int(i)-1] == '14' or str[int(i)] == '6':#Находим слагаемые
            summand(str, result)#Переходим в <слагаемые>

def summand(str, result):#<слагаемые> -> здесь ищем <слагаемые>/<множители>/*/div
    j=0
    for i, value in enumerate(str):
        if str[int(i)] == '6' : #Находим первое выражение (M+1/N)
            result.append(config['6'])#Записываем div в массив
            for i, value in enumerate(str):
                if str[int(i)] == '7' and str[int(i) - 5] == '14':  # Находим слагаемое, внутри которого <множитель>->ид/конст
                    result.append(str[int(i) - 4])  # Записываем значение первого множителя, т.е. ид/конст (1)
                    result.append(ids['1'])  # Записываем значение второго множителя, т.е. ид/конст (N)
                    for i, value in enumerate(str):
                        if str[int(i)] == '2' and str [int(i) - 1] == '13':#Находим слагаемое
                            j = i + 6
                            result.append(ids['2'])#Записываем в массив (M)
                            list_of_operators((str[:(i)-1] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы

        if str[int(i)] == '8' : #Находим второе выражение (M*N+3)
            result.append(config['8'])#Записываем * в массив
            for i, value in enumerate(str):
                if str[int(i)] == '1' and str[int(i) - 4] == '13':# Находим слагаемое, внутри которого <множитель>->ид/конст
                    result.append(ids['2'])#Записываем первый множитель (M)
                    result.append(ids['1'])#Записываем второй множитель (N)
                    for i, value in enumerate(str):
                        if str[int(i)] == '3' and str[int(i) - 1] == '14':#Находим второе слагаемое
                            j = i + 1
                            result.append(str[int(i)])#Записываем в массив (3)
                            list_of_operators((str[:(i) - 6] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы

def conclusion(str, result):#<вывод> -> здесь ищем write(идентификатор)
    j = 0
    for i, value in enumerate(str):
        if str[int(i)] == '12':#Находим закрывающую скобку
            j = i + 1
            result.append(config['10'])#Добавляем в массив write
            result.append(config['11'])#Добавляем в массив (
            result.append(ids['1'])#Добавляем в массив N
            result.append(config['12'])#Добавляем в массив )
            list_of_operators((str[:(i) - 4] + str[j:]), result)#Возвращаемся в начало, срезав найденные элементы


result_file = open('TextLR2.txt', 'w')
list_of_operators(work_str.split(), result)
result_file.close()