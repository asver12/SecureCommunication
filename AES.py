import LFSR
import helper
import mathematics
from bitarray import bitarray


class AES():
    def __init__(self, key):
        self.irreducable_polynome = "100011011"  # [1, 1, 0, 1, 1, 0, 0, 0, 1]
        self.SBox = [
            [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
            [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
            [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
        ]

        self.inv_SBox = [
            [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
            [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
            [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
            [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
            [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
            [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
            [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
            [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
            [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
            [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
            [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
            [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
            [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
            [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
            [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]
        ]

        self.mix_columns_matrix = [
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ]

        self.inv_mix_columns_matrix = [
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ]

        self.RC = (
            0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F, 0x5E,
            0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A, 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
        )

        self.keys = self.gen_all_round_keys(key)

    def __convert_text2bin__(self, text):
        matrix = [[], [], [], []]
        for i in range(16):
            matrix[i % 4].append(bin(ord(text[i])))
        return matrix

    def __convert_bin2text__(self, matrix):
        text = ""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                text += chr(int(matrix[j][i], base=2))
        return text

    def add_roundkey(self, matrix, roundkey, verbose=False):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if verbose:
                    print("{}-{}".format(i, j))
                    print("{}^{} = {}".format(matrix[i][j],
                                              "".join(str(x) for x in roundkey[(len(matrix) * j * 8 + i * 8):(
                                                      (len(matrix) * j * 8 + i * 8) + 8)]), bin(
                            int("".join(str(x) for x in
                                        roundkey[(len(matrix) * j * 8 + i * 8):((len(matrix) * j * 8 + i * 8) + 8)]),
                                base=2) ^ int(
                                matrix[i][j], base=2))))
                matrix[i][j] = bin(int("".join(
                    str(x) for x in roundkey[(len(matrix) * j * 8 + i * 8):((len(matrix) * j * 8 + i * 8) + 8)]),
                    base=2) ^ int(matrix[i][j], base=2))
        return matrix

    def __xor_lists__(self,list_1,list_2):
        erg = []
        for i,j in zip(list_1,list_2):
            erg.append(str(int(i)^int(j)))
        return erg

    def gen_round_key(self, key, round=1, verbose=False):
        if verbose:
            print("________----------------________")
            print("ROUND: {}".format(round))
            print("Key[{}]: {}:{}".format(round - 1, helper.get_split_string_from_list(key), len(key)))
        key = list(key)
        if verbose:
            print("G: Key: {}:{}".format(helper.get_split_string_from_list(key[-32:]), len(key[-32:])))
        shift_key = helper.shift(key[-32:], 8)
        if verbose:
            print("G: Shifted-Key: {}:{}".format(helper.get_split_string_from_list(shift_key), len(shift_key)))
            print("G: RC: {}:{}".format('{0:08b}'.format(self.RC[round]), len('{0:08b}'.format(self.RC[round]))))
            print("G: V1: {}:{}".format("".join(shift_key[0:8]), len(shift_key[0:8])))
        shift_key[0:8] = list('{0:08b}'.format(int("".join(shift_key[0:8]), base=2) ^ self.RC[round]))
        if verbose:
            print("G:     " + "".join(shift_key[0:8]))
            print("G: Key:{}:{}".format(helper.get_split_string_from_list(shift_key), len(shift_key)))
        key[0:32] = shift_key
        for i in range(32, len(key) - 1, 32):
            if verbose:
                print("--------------------------------")
                print("W[{}] ^ W[{}]:".format(int(((i / 32) - 1) * round), int((i / 32) * round)))
                print("{}:{}".format(helper.get_split_string_from_list(key[(i - 32):i]), len(key[(i - 32):i])))
                print("{}:{}".format(helper.get_split_string_from_list(key[i:(i + 32)]),
                                     len(key[i:(i + 32)])))
            key[i:(i + 32)] = self.__xor_lists__(key[(i - 32):i], key[i:(i + 32)])
            if verbose:
                print("{}:{}".format(helper.get_split_string_from_list(key[i:(i + 32)]),
                                     len(key[i:(i + 32)])))
        if verbose:
            print("Key[{}]: {}:{}".format(round, helper.get_split_string_from_list(key), len(key)))
        return "".join(key)

    def gen_all_round_keys(self, key, verbose=False):
        if verbose:
            print("____All Round-Keys____")
            print("Round 0:\t{}".format(helper.get_split_string_from_list(key)))
        keys = [key]
        for i in range(1, 11):
            key = self.gen_round_key(key, i)
            if verbose:
                print("Round {}:\t{}".format(i, helper.get_split_string_from_list(key)))
            keys.append(key)
        return keys

    def substitute_bytes(self, hex_matrix, verbose=False):
        if verbose:
            print("---Substitute bytes--")
        hex_matrix = self.__substitute_bytes__(hex_matrix, self.SBox)
        if verbose:
            print("--------------------")
        return hex_matrix

    def inv_substitute_bytes(self, hex_matrix, verbose=False):
        if verbose:
            print("-Inv Substitute bytes-")
        hex_matrix = self.__substitute_bytes__(hex_matrix, self.inv_SBox)
        if verbose:
            print("--------------------")
        return hex_matrix

    def __substitute_bytes__(self, hex_matrix, sBox, verbose=False):
        for i in hex_matrix:
            for j in range(len(i)):
                if verbose:
                    print("{} -> {}".format(helper.convert_bin_to_hex(i[j]), hex(
                        sBox[helper.get_hex_position_from_bin(i[j], 0)][helper.get_hex_position_from_bin(i[j], 1)])))
                i[j] = bin(
                    sBox[helper.get_hex_position_from_bin(i[j], 0)][helper.get_hex_position_from_bin(i[j], 1)])
        return hex_matrix

    def shift_rows(self, hex_matrix):
        for i in range(1, len(hex_matrix)):
            hex_matrix[i] = helper.shift(hex_matrix[i], i)
        return hex_matrix

    def mix_column(self, column, matrix, verbose=False):
        new_column = []
        if verbose:
            print("-----Mix Column------")
            print(" ".join([str(helper.convert_bin_to_hex(x)) for x in column]))
        for i in range(len(column)):
            erg = 0
            for j in range(len(matrix)):
                if verbose:
                    print("{}*{} ".format(matrix[i][j], column[j]), end="")
                in_between = int(mathematics.mult(int(column[j], base=2), matrix[i][j]), base=2)
                in_between_1 = int(mathematics.binary_devision(in_between,
                                                               int(self.irreducable_polynome, base=2))[0], base=2)
                erg ^= in_between_1
                if verbose:
                    print("[={}] ".format(bin(in_between_1)), end="")
            erg = mathematics.binary_devision(erg, int(self.irreducable_polynome, base=2))[0]
            if verbose:
                print("= {}".format(erg))
            new_column.append(erg)
        if verbose:
            print("---------------------")
        return new_column

    def mix_columns(self, hex_matrix, verbose=False):
        if verbose:
            print("----Mix Columns------")
        for index, item in enumerate(list(map(list, zip(*hex_matrix)))):
            mixed_colum = self.mix_column(item, self.mix_columns_matrix, verbose=verbose)
            # for j in range(len(mixed_colum)):
            for i in range(4):
                hex_matrix[i][index] = mixed_colum[i]
        return hex_matrix

    def inv_mix_columns(self, hex_matrix, verbose=False):
        if verbose:
            print("---Inv Mix Columns--")
        for index, item in enumerate(list(map(list, zip(*hex_matrix)))):
            mixed_colum = self.mix_column(item, self.inv_mix_columns_matrix, verbose=verbose)
            for j in range(len(mixed_colum)):
                hex_matrix[j][index] = mixed_colum[j]
        return hex_matrix

    def inv_shift_rows(self, hex_matrix, verbose=False):
        for i in range(1, len(hex_matrix)):
            hex_matrix[i] = helper.shift(hex_matrix[i], -i)
        return hex_matrix

    def decrypt(self, text, verbose=False):
        converter = self.__convert_text2bin__(text)
        if verbose:
            print("Text: {}".format(text))
            print("Key: {}".format(helper.get_split_string_from_list(list(self.keys[10]))))
            print("After Convertion:")
            self.print_matrix_as_hex(converter)
            print("")
            print("__________Round 0_________")

        added_round_key = self.add_roundkey(converter, self.keys[10])  # , verbose=verbose)

        if verbose:
            print("After Roundkey")
            self.print_matrix_as_hex(added_round_key)
        for i in range(1, 10):
            if verbose:
                print("")
                print("__________Round {}_________".format(i))

            after_shift = self.inv_shift_rows(added_round_key)  # , verbose=verbose)

            if verbose:
                print("After RowShift:")
                self.print_matrix_as_hex(after_shift)

            after_substitution = self.inv_substitute_bytes(after_shift)

            if verbose:
                print("After Substitution:")
                self.print_matrix_as_hex(after_substitution)
            if verbose:
                print("New Roundkey:")
                print(helper.get_split_string_from_list(self.keys[10 - i]))

            added_round_key = self.add_roundkey(after_substitution, self.keys[10 - i])  # , verbose=verbose)

            if verbose:
                print("After Roundkey")
                self.print_matrix_as_hex(added_round_key)

            after_mix_columns = self.inv_mix_columns(added_round_key)  # , verbose=verbose)

            if verbose:
                print("After MixColumns:")
                self.print_matrix_as_hex(after_mix_columns)

        if verbose:
            print("__________Round 10________")

        after_shift = self.inv_shift_rows(after_mix_columns)

        if verbose:
            print("After RowShift:")
            self.print_matrix_as_hex(after_shift)

        after_substitution = self.inv_substitute_bytes(after_shift)

        if verbose:
            print("After Substitution:")
            self.print_matrix_as_hex(after_substitution)
        if verbose:
            print("New Roundkey:")
            print(helper.get_split_string_from_list(self.keys[0]))

        added_round_key = self.add_roundkey(after_substitution, self.keys[0])  # , verbose=verbose)

        if verbose:
            print("After Roundkey")
            self.print_matrix_as_hex(added_round_key)

        return self.__convert_bin2text__(added_round_key)

    def encrypt(self, text, verbose=False):
        converter = self.__convert_text2bin__(text)
        if verbose:
            print("Text: {}".format(text))
            print("Key: {}".format(helper.get_split_string_from_list(list(self.keys[0]))))
            print("After Convertion:")
            self.print_matrix_as_hex(converter)
            print("")
            print("__________Round 0_________")
        added_round_key = self.add_roundkey(converter, self.keys[0])  # , verbose=verbose)
        if verbose:
            print("After Roundkey")
            self.print_matrix_as_hex(added_round_key)
        for i in range(1, 10):
            if verbose:
                print("")
                print("__________Round {}_________".format(i))

            after_substitution = self.substitute_bytes(added_round_key)

            if verbose:
                print("After Substitution:")
                self.print_matrix_as_hex(after_substitution)

            after_shift = self.shift_rows(after_substitution)

            if verbose:
                print("After RowShift:")
                self.print_matrix_as_hex(after_shift)

            after_mix_columns = self.mix_columns(after_shift)  # , verbose=verbose)

            if verbose:
                print("After MixColumns:")
                self.print_matrix_as_hex(after_mix_columns)
            if verbose:
                print("New Roundkey:")
                print(helper.get_split_string_from_list(self.keys[i]))

            added_round_key = self.add_roundkey(after_mix_columns, self.keys[i])  # , verbose=verbose)

            if verbose:
                print("After Roundkey")
                self.print_matrix_as_hex(added_round_key)
        if verbose:
            print("__________Round 10________")

        after_substitution = self.substitute_bytes(added_round_key)

        if verbose:
            print("After Substitution:")
            self.print_matrix_as_hex(after_substitution)

        after_shift = self.shift_rows(after_substitution)

        if verbose:
            print("After RowShift:")
            self.print_matrix_as_hex(after_shift)
        if verbose:
            print("New Roundkey:")
            print(helper.get_split_string_from_list(self.keys[10]))

        added_round_key = self.add_roundkey(after_shift, self.keys[10])  # , verbose=verbose)

        if verbose:
            print("After Roundkey")
            self.print_matrix_as_hex(added_round_key)

        return self.__convert_bin2text__(added_round_key)

    def print_matrix_as_hex(self, matrix):
        for i in matrix:
            print("[ " + ' '.join(helper.convert_bin_to_hex(x) for x in i) + " ]")

    def first_and_last_round(self,text, key):

        converter = aes.__convert_text2bin__(text)
        print("After Convertion:")
        aes.print_matrix_as_hex(converter)
        added_round_key = aes.add_roundkey(converter, key)
        print("After Roundkey")
        aes.print_matrix_as_hex(added_round_key)
        after_substitution = aes.substitute_bytes(added_round_key, verbose=True)
        print("After Substitution:")
        aes.print_matrix_as_hex(after_substitution)
        after_shift = aes.shift_rows(after_substitution)
        print("After RowShift:")
        aes.print_matrix_as_hex(after_shift)
        after_mix_columns = aes.mix_columns(after_shift, verbose=True)
        print("After MixColumns:")
        aes.print_matrix_as_hex(after_mix_columns)

        key_gen = aes.gen_round_key(key, verbose=True)
        print("New Key:")
        print(helper.get_split_string_from_list(key_gen))
        encryption = aes.add_roundkey(after_mix_columns, key_gen, verbose=True)
        print("Encryption:")
        aes.print_matrix_as_hex(encryption)

        print("Decryption:")
        added_round_key = aes.add_roundkey(encryption, key_gen, verbose=True)
        print("After Roundkey:")
        aes.print_matrix_as_hex(added_round_key)
        after_mix_columns = aes.inv_mix_columns(added_round_key, verbose=True)
        print("After MixColumns:")
        aes.print_matrix_as_hex(after_mix_columns)

        after_shift = aes.inv_shift_rows(after_mix_columns)
        print("After RowShift:")
        aes.print_matrix_as_hex(after_shift)

        after_substitution = aes.inv_substitute_bytes(after_shift)
        print("After Substitution:")
        aes.print_matrix_as_hex(after_substitution)
        added_round_key = aes.add_roundkey(encryption, key)
        print("After Roundkey:")
        aes.print_matrix_as_hex(added_round_key)
        print(aes.__convert_bin2text__(added_round_key))

if __name__ == "__main__":
    startzustand = [1, 1, 1, 1, 0, 0, 0, 0]
    a = bitarray(startzustand)
    start_lfsr = LFSR.lfsr(a, [0, 1, 3, 4])
    key = [next(start_lfsr) for _ in range(120)]
    key = "".join(str(x) for x in startzustand + key)
    aes = AES(key)
    aes.gen_all_round_keys(key, verbose=True)
    # encryption = aes.encrypt("securityisnoeasy", verbose=True)
    # print("Encryption: {}".format(encryption))
    # print(encryption)
    # decryption = aes.decrypt(encryption, verbose=True)
    # print(decryption)
    print("Testrechnung: ")
    aes.first_and_last_round("securityisnoeasy",key)
