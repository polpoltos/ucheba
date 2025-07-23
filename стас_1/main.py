def OpenFile():
    str_list = []
    with open("test.txt", "r", encoding="utf-8") as file:
        for line in file:
            str_list.append(list(line.strip()))

    return str_list

def Polibiy(str_list, message):
    new_mes = ""
    message_list = list(message)
    print(str_list)
    if 'Б' in str_list:
        print("cool")
    else:
        print("not")

def main():
    message = "привет"
    str_list = OpenFile()
    Polibiy(str_list, message)

if __name__ == "__main__":
    main()