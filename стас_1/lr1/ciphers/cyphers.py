import math


class Ciphers:
    class Caesar:
        def run(self, text: str, shift: int, decode: bool = False) -> str:
            if decode:
                shift = -shift

            result = []

            for char in text:
                if char.isalpha():
                    shift_base = ord("A") if char.isupper() else ord("a")
                    shifted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
                    result.append(shifted_char)
                else:
                    result.append(char)

            return "".join(result)

    class Crossword:
        def __encode(self, text):
            if math.sqrt(len(text)) <= 5:
                n = 5
            else:
                n = math.ceil(math.sqrt(len(text)))

            a = ["_"] * n
            for i in range(n):
                a[i] = ["_"] * n

            text = text.replace(" ", "_")
            t = 0

            for i in range(0, n):
                for j in range(n * (i % 2) - i % 2, n * ((i + 1) % 2) - i % 2, 1 - (i % 2) * 2):
                    if t < len(text):
                        a[j][i] = text[t]
                        t += 1

            result = ""

            for i in range(n):
                for j in range(n):
                    result += a[i][j]
            return result

        def __decode(self, text):
            if math.sqrt(len(text)) <= 5:
                n = 5
            else:
                n = math.ceil(math.sqrt(len(text)))

            a = ["_"] * n
            for i in range(n):
                a[i] = ["_"] * n

            t = 0

            for i in range(n):
                for j in range(n):
                    if t < len(text):
                        a[i][j] = text[t]
                        t += 1

            result = ""
            for i in range(0, n):
                for j in range(n * (i % 2) - i % 2, n * ((i + 1) % 2) - i % 2, 1 - (i % 2) * 2):
                    result += a[j][i]
            result = result.replace("_", " ").strip()
            return result

        def run(self, text: str, decode=False):
            return self.__encode(text) if not decode else self.__decode(text)

    class Gamma:
        alphabet = []
        N = 27

        def __init__(self):
            self.alphabet = self.__generate_alphabet()

        def __generate_alphabet(self):
            alphabet = []
            for i in range(ord("a"), ord("z") + 1):
                alphabet.append(chr(i))
            alphabet.append(" ")
            return alphabet

        def __encode(self, text, gamma):
            text_len = len(text)
            gamma_len = len(gamma)

            key_text = []
            for i in range(text_len // gamma_len):
                for char in gamma:
                    key_text.append(char)
            for i in range(text_len % gamma_len):
                key_text.append(gamma[i])

            code = []
            for i in range(text_len):
                t_i = self.alphabet.index(text[i])
                g_i = self.alphabet.index(key_text[i])

                code.append(self.alphabet[(t_i + g_i) % self.N])

            return "".join(code)

        def __decode(self, code, gamma):
            code_len = len(code)
            gamma_len = len(gamma)

            key_text = []
            for i in range(code_len // gamma_len):
                for char in gamma:
                    key_text.append(char)
            for i in range(code_len % gamma_len):
                key_text.append(gamma[i])

            text = []
            for i in range(code_len):
                t_i = self.alphabet.index(code[i])
                g_i = self.alphabet.index(key_text[i])
                text.append(self.alphabet[(t_i - g_i + self.N) % self.N])

            return "".join(text)

        def run(self, text: str, gamma, decode=False):
            return self.__encode(text, gamma) if not decode else self.__decode(text, gamma)

    class ADFGVX:
        adfgvx = "ADFGVX"
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        substitution_key = None
        transposition_key = None
        polybius_square = None

        def set_substitution_key(self, substitution_key):
            if self.__create_polybius_square(substitution_key):
                self.substitution_key = substitution_key

        def set_transposition_key(self, transposition_key):
            self.transposition_key = transposition_key

        def __create_polybius_square(self, key):
            key = "".join(sorted(set(key.upper()), key=key.upper().index))

            remaining_chars = [char for char in self.alphabet if char not in key]
            remaining_chars = "".join(remaining_chars)

            self.polybius_square = key + remaining_chars

            print("Polibius square:")
            for i in range(6):
                print(self.polybius_square[i * 6 : (i + 1) * 6])

            return True

        def __encrypt(self, text):
            encrypted_text = ""

            for char in text:
                if char.upper() in self.polybius_square:
                    index = self.polybius_square.index(char.upper())
                    row = self.adfgvx[index // 6]
                    column = self.adfgvx[index % 6]
                    encrypted_text += row + column

            for i in range(len(self.transposition_key)):
                print(encrypted_text[i * len(self.transposition_key) : (i + 1) * len(self.transposition_key)])

            transposed_text = [""] * len(self.transposition_key)
            for i, _ in enumerate(encrypted_text):
                transposed_text[i % len(self.transposition_key)] += encrypted_text[i]

            indexed_transposition_key = [f"{char}{i}" for i, char in enumerate(self.transposition_key)]
            print(f"indexed_transposition_key: {indexed_transposition_key}")

            transposed_text = [
                x
                for _, x in sorted(
                    zip(indexed_transposition_key, transposed_text),
                    key=lambda pair: pair[0],
                )
            ]

            return "".join(transposed_text)

        def __decrypt(self, encrypted_text):
            full_columns = len(encrypted_text) % len(self.transposition_key)

            chars_per_column = len(encrypted_text) // len(self.transposition_key)

            columns = [""] * len(self.transposition_key)

            indexed_transposition_key = [f"{char}{i}" for i, char in enumerate(self.transposition_key)]
            i = 0
            for key in sorted(indexed_transposition_key):
                length = (
                    chars_per_column + 1 if indexed_transposition_key.index(key) < full_columns else chars_per_column
                )
                columns[indexed_transposition_key.index(key)] = encrypted_text[i : i + length]
                i += length

            decrypted_text = ""
            max_len = max(len(column) for column in columns)
            for i in range(max_len):
                for column in columns:
                    if i < len(column):
                        decrypted_text += column[i]

            i = 0
            while i < len(decrypted_text):
                row = decrypted_text[i]
                column = decrypted_text[i + 1]
                index = self.adfgvx.index(row) * 6 + self.adfgvx.index(column)
                if index < len(self.polybius_square):
                    decrypted_text = decrypted_text[:i] + self.polybius_square[index] + decrypted_text[i + 2 :]
                i += 1

            return decrypted_text

        def run(self, text, decode=False):
            return self.__encrypt(text) if not decode else self.__decrypt(text)
