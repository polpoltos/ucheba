hard_dictionary = {"А": "11", "Б": "12", "В": "13",
                   "Г": "14", "Д": "15", "Е": "16", "Ё": "21",
                   "Ж": "22", "З": "23", "И": "24", "Й": "25",
                   "К": "26", "Л": "31", "М": "32", "Н": "33",
                   "О": "34", "П": "35", "Р": "36", "С": "41",
                   "Т": "42", "У": "43", "Ф": "44", "Х": "45",
                   "Ц": "46", "Ч": "51", "Ш": "52", "Щ": "53",
                   "Ъ": "54", "Ы": "55", "Ь": "56", "Э": "61",
                   "Ю": "62", "Я": "63", " ": "64"}


def code(mes):
    list_mes = list(mes.upper())
    res = []
    for x in list_mes:
        if x in hard_dictionary:
            value_mes = int(hard_dictionary.get(x))
            if 54 <= value_mes <= 56:
                code_txt = str(value_mes - 40)
            elif 57 <= value_mes <= 64:
                code_txt = str(value_mes - 50)
            else:
                code_txt = str(value_mes + 10)
            for key in hard_dictionary:
                if hard_dictionary[key] == code_txt:
                    res.append(key)
        else:
            print("Символ не найден")
            break

    return "".join(res)


def decode(code_txt):
    list_mes = list(code_txt.upper())
    res = []
    for x in list_mes:
        if x in hard_dictionary:
            value_mes = int(hard_dictionary.get(x))
            if 15 <= value_mes <= 16:
                code_txt = str(value_mes + 40)
            elif 11 <= value_mes <= 14:
                code_txt = str(value_mes + 50)
            else:
                code_txt = str(value_mes - 10)
            for key in hard_dictionary:
                if hard_dictionary[key] == code_txt:
                    res.append(key)
        else:
            print("Символ не найден")
            break
    return "".join(res)


def main():
    mes = input("Введите сообщение: ")
    code_txt = code(mes)
    print(f"Исходное сообщение: {mes.upper()}")
    print(f"Закодированное сообщение: {code_txt}")
    decode_txt = decode(code_txt)
    print(f"Раскодированное сообщение: {decode_txt}")


if __name__ == "__main__":
    main()
