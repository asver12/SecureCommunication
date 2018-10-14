def shift(l, n):
    return l[n:] + l[:n]

def hex_to_int(n):
    return int("".join(n.split(":")), 16)

def get_hex_position_from_bin(binary_number, i):
    return int(binary_number[2:].zfill(8)[i * 4:i * 4 + 4], base=2)


def get_bin_from_str(hex_str):
    return bin(int(hex_str.encode("ascii"), base=16))


def get_int_from_list(bin_list):
    return int("".join(str(int(item)) for item in bin_list), 2)


def get_split_string_from_list(binary_string):
    return " ".join(str("".join(str(x) for x in binary_string[i:i + 8])) for i in range(0, len(binary_string), 8))


def get_bin_from_list(bin_list):
    return bin(int("".join(str(int(item)) for item in bin_list), 2))


def convert_bin_to_hex(bin):
    return hex(int(bin, base=2))
