from ciphers.cyphers import Ciphers


class Output:
    ciphers = Ciphers()

    def __print_results(self, title, encoded, decoded):
        print(f"\n{title}\n")
        print(f"Encoded text: {encoded}")
        print(f"Decoded text: {decoded}\n")

    def __caesar(self, text: str, shift: int = 3):
        init = self.ciphers.Caesar()

        encoded = init.run(text, shift)
        decoded = init.run(encoded, shift, decode=True)

        self.__print_results("CAESAR", encoded, decoded)

    def __crossword(self, text: str):
        init = self.ciphers.Crossword()

        encoded = init.run(text)
        decoded = init.run(encoded, decode=True)

        self.__print_results("CROSSWORD", encoded, decoded)

    def __gamma(self, text: str, gamma: str):
        init = self.ciphers.Gamma()

        encoded = init.run(text, gamma)
        decoded = init.run(encoded, gamma, decode=True)

        self.__print_results("GAMMA", encoded, decoded)

    def __avdgvx(self, text: str):
        init = self.ciphers.ADFGVX()

        substitution_key = input("Insert substitution key:")
        init.set_substitution_key(substitution_key)
        transposition_key = input("Insert transposition key:")
        init.set_transposition_key(transposition_key)

        encoded = init.run(text)
        decoded = init.run(encoded, decode=True)

        self.__print_results("ADFGVX", encoded, decoded)

    def run(self, text):
        self.__caesar(text)
        self.__crossword(text)
        self.__gamma(text, input("Insert gamma key:"))
        self.__avdgvx(text)
