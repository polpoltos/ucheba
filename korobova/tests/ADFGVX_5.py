from random import shuffle, choice
from itertools import product, accumulate
from numpy import floor, sqrt
from texttable import Texttable

import string
from itertools import cycle


# Полибийский квадрат
def create_polybius_square():
    chars = string.ascii_uppercase + string.digits
    key = 'ADFGVX'
    square = {}
    index = 0
    for r in key:
        for c in key:
            square[chars[index]] = (r, c)
            index += 1
    return square, chars


# Функция для печати полибийского квадрата
def print_polybius_square(square, chars):
    key = 'ADFGVX'
    table = [['' for _ in range(6)] for _ in range(6)]

    index = 0
    for r in range(6):
        for c in range(6):
            table[r][c] = chars[index]
            index += 1

    print("  | " + " | ".join(key) + " |")
    print("--+" + "---+" * 6)
    for r in range(6):
        print(f"{key[r]} | " + " | ".join(table[r]) + " |")


class ADFGVX:
    def __init__(self, spoly, k, alph='ADFGVX'):
        self.polybius = list(spoly.upper())
        self.pdim = int(floor(sqrt(len(self.polybius))))
        self.key = list(k.upper())
        self.keylen = len(self.key)
        self.alphabet = list(alph)
        pairs = [p[0] + p[1] for p in product(self.alphabet, self.alphabet)]
        self.encode = dict(zip(self.polybius, pairs))
        self.decode = dict((v, k) for (k, v) in self.encode.items())

    def encrypt(self, msg):
        tm1 = Texttable()
        st = [i for i in self.key]
        tm1.add_row(st)
        t1 = []

        chars = list(''.join([self.encode[c] for c in msg.upper() if c in self.polybius]))
        count = 0
        for i in chars:
            t1.append(i)
            if count == self.keylen-1:
                tm1.add_row(t1)
                t1 = []
                count = 0
            else:
                count += 1
        print("Таблица перестановочная")
        print(tm1.draw())

        colvecs = [(lett, chars[i:len(chars):self.keylen]) for (i, lett) in enumerate(self.key)]
        colvecs.sort(key=lambda x: x[0])
        return ''.join([''.join(a[1]) for a in colvecs])

    def decrypt(self, cod):
        chars = [c for c in cod if c in self.alphabet]
        sortedkey = sorted(self.key)
        order = [self.key.index(ch) for ch in sortedkey]
        originalorder = [sortedkey.index(ch) for ch in self.key]
        base, extra = divmod(len(chars), self.keylen)
        strides = [base + (1 if extra > i else 0) for i in order]
        starts = list(accumulate(strides[:-1], lambda x, y: x + y))
        starts = [0] + starts
        ends = [starts[i] + strides[i] for i in range(self.keylen)]
        cols = [chars[starts[i]:ends[i]] for i in originalorder]
        pairs = []
        for i in range((len(chars) - 1) // self.keylen + 1):
            for j in range(self.keylen):
                if i * self.keylen + j < len(chars):
                    pairs.append(cols[j][i])

        return ''.join([self.decode[pairs[i] + pairs[i + 1]] for i in range(0, len(pairs), 2)])


if __name__ == '__main__':
    PCHARS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    shuffle(PCHARS)
    POLYBIUS = ''.join(PCHARS)
    KEY = input("Введите ключ (ENG):")

    SECRET, MESSAGE = ADFGVX(POLYBIUS, KEY), input("Введите сообщение (ENG):")

    tm = Texttable()
    t = []
    count = 0
    for c in POLYBIUS:
        t.append(c)
        if count == 6:
            tm.add_row(t)
            t = []
            count = 0
        else:
            count += 1
    print("Таблица шифрозамен")
    polybius_square, chars = create_polybius_square()
    print_polybius_square(polybius_square, chars)
    print(f'Ключ: {KEY}')
    print('Сообщение: ', MESSAGE)
    ENCODED = SECRET.encrypt(MESSAGE)
    DECODED = SECRET.decrypt(ENCODED)
    print('Закодировано: ', ENCODED)
    print('Раскодировано: ', DECODED)
