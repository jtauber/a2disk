# Applesoft BASIC de-tokenizer
# James Tauber / jtauber.com


import sys


def token(d):
    return {
        0x80: "END",
        0x81: "FOR",
        0x82: "NEXT",
        0x83: "DATA",
        0x84: "INPUT",
        0x86: "DIM",
        0x87: "READ",
        0x89: "TEXT",
        0x8A: "PR #",
        0x8B: "IN #",
        0x8C: "CALL",
        0x91: "HGR",
        0x92: "HCOLOR=",
        0x93: "HPLOT",
        0x96: "HTAB",
        0x97: "HOME",
        0x9D: "NORMAL",
        0x9E: "INVERSE",
        0xA2: "VTAB",
        0xA3: "HIMEM:",
        0xA5: "ONERR",
        0xAB: "GOTO",
        0xAD: "IF",
        0xB0: "GOSUB",
        0xB1: "RETURN",
        0xB2: "REM",
        0xB4: "ON",
        0xB9: "POKE",
        0xBA: "PRINT",
        0xBD: "CLEAR",
        0xBE: "GET",
        0xC0: "TAB",
        0xC1: "TO",
        0xC3: "SPC(",
        0xC4: "THEN",
        0xC7: "STEP",
        0xC8: "+",
        0xC9: "-",
        0xCA: "*",
        0xCB: "/",
        0xCC: ";",
        0xCD: "AND",
        0xCE: "OR",
        0xCF: ">",
        0xD0: "=",
        0xD1: "<",
        0xD2: "SGN",
        0xD3: "INT",
        0xD4: "ABS",
        0xD6: "FRE",
        0xDA: "SQR",
        0xDB: "RND",
        0xE1: "ATN",
        0xE2: "PEEK",
        0xE3: "LEN",
        0xE4: "STR$",
        0xE5: "VAL",
        0xE7: "CHR$",
    }[d]


class Detokenize:

    def __init__(self, data):
        self.data = data
        self.index = 0

    def read_byte(self):
        d = self.data[self.index]
        self.index += 1
        return d

    def read_word(self):
        return self.read_byte() + 0x100 * self.read_byte()

    def detokenize(self):
        length = self.read_word()

        while self.index < length:
            memory = self.read_word()
            line_number = self.read_word()

            sys.stdout.write("{} ".format(line_number))
            while True:
                d = self.read_byte()
                if d == 0x00:
                    print()
                    break
                elif d <= 0x7F:
                    sys.stdout.write(chr(d))
                else:
                    sys.stdout.write(" {} ".format(token(d)))


class ApplesoftHandler:

    def __init__(self):
        self.data = []

    def __enter__(self):
        return self.receive_sector_data

    def __exit__(self, exc_type, exc_value, traceback):
        Detokenize(self.data).detokenize()

    def receive_sector_data(self, sector_data):
        self.data += sector_data
