import config


def main():
    spisok = []
    with open('config.txt', 'r', encoding='utf-8') as f:
        for code_line in f:
            for word in code_line.split():
                line = ''
                for i in word:
                    line += config.config[i] + '-'
                spisok.append(line[:-1])
            print("_".join(spisok))



if __name__ == '__main__':
    main()
