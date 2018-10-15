# Generate secure random numbers
import secrets
from bitarray import bitarray
import itertools
import helper


def gcd(n, e):
    while e:
        n, e = e, n % e
    return n


def extended_gcd(a, b, verbose=False):
    """
    Gibt das Ergebniss des Euklidischen Algorithmus zurück:
    gcd(a, b) = a * s + b * t
    :param a: erste Zahl im Euklidischen Algorithmus
    :param b: zweite Zahl im Euklidischen Algorithmus
    :return: gcd, s, t
    """
    u = 1
    # s is not required for RSA
    s = 0

    v = 0
    t = 1
    while b:
        a, b, q = b, a % b, a // b
        u, s = s, u - q * s
        v, t = t, v - q * t
    return a, u, v


def mult_with_2(binary_number):
    return int(binary_number, base=2) << 1


def mult_with_3(binary_number):
    return (int(binary_number, base=2) << 1) + int(binary_number, base=2)


def mult(polynome_1, polynome_2, verbose=False):
    if polynome_1 == 0 or polynome_2 == 0:
        return bin(0)
    new_polynome = [0 for _ in range(polynome_1.bit_length() + polynome_2.bit_length() - 1)]
    if verbose:
        print("Polynome 1: {}".format(bin(polynome_1)[2:]))
        print("Polynome 2: {}".format(bin(polynome_2)[2:]))
    for index_i, elem_i in enumerate(bin(polynome_1)[2:]):
        for index_j, elem_j in enumerate(bin(polynome_2)[2:]):
            if verbose:
                print("{} ^= {}&{}[{},{}]".format(new_polynome[index_i + index_j], elem_i, elem_j, index_i, index_j))
            new_polynome[index_i + index_j] ^= int(elem_i) & int(elem_j)
            if verbose:
                "1100 1110"
                print(helper.get_split_string_from_list(new_polynome))
    return bin(int("".join(str(x) for x in new_polynome), base=2))


def add(polynome_1, polynome_2, field=2):
    return [sum(x) % field for x in itertools.zip_longest(polynome_1, polynome_2, fillvalue=0)]


def binary_division(zaehler, nenner, verbose=False):
    if zaehler == 0 or nenner == 0:
        return bin(0), bin(0)

    def get_degree(polynome):
        return polynome.bit_length() - bitarray(bin(polynome)[2:]).index(1)

    nenner_deg = get_degree(nenner)
    zaehler_degree = get_degree(zaehler)
    erg = 0
    if verbose:
        print("Grad Nenner: {}".format(nenner_deg))
    while zaehler_degree >= nenner_deg:
        exponent = zaehler_degree - nenner_deg
        teiler = nenner << exponent
        if verbose:
            print("Grad Zaehler: {}".format(zaehler_degree))
            print("Exponent: {}".format(exponent))
            print("Zaehler: {}".format(bin(zaehler)))
            print("Teiler: {}".format(bin(teiler)))
        erg ^= 1 << (exponent)
        if verbose:
            print("Zwischenergebnis: {}".format(bin(erg)))
        zaehler ^= teiler
        zaehler_degree = get_degree(zaehler)
    return bin(zaehler), bin(erg)

def bitshift(binary_number, shift):
    return bitarray(bin((int(binary_number.to01().encode(), base=2) << shift))[2:])


def calc_mod_inv(e, phi_n):
    """
    Calc the inv to e*d === mod phi_n
    :param e: public exponent
    :param phi_n: Phi of n ( n = p*q )
    :return: private_key ( d )
    """

    pass


def square_and_multiply_for_modular(x, exponent, n, verbose=False):
    """
    Optimized Modular-Calculation
    Only turn verbose one when using smal examples

    :param x: basis-element
    :param exponent: Exponent such that as less 1. as possible in its binary representation
    :param n: modulus
    :return:
    """
    r = x
    bin_exp = bin(exponent)[2:][::-1]
    if verbose:
        print("--Square and multiply--")
        print("{}^{}".format(r, bin_exp))
    for i in range(exponent.bit_length() - 2, -1, -1):
        if verbose:
            print("{}^2 mod {} = {}".format(r, n, (r ** 2) % n))
        r = (r ** 2) % n
        if bin_exp[i] == "1":
            if verbose:
                print("[i:{}] {}*{} mod {} = {}".format(i, r, x, n, r * x % n))
            r = r * x % n
    return r


if __name__ == "__main__":
    print("gcd[122,22]:{}, {}, {}".format(*extended_gcd(122, 22)))
    print("gcd[120,23]:{}, {}, {}".format(*extended_gcd(120, 23)))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(5, 4, 12), (5 ** 4) % 12))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(12, 18, 9), (12 ** 18) % 9))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(4, 3, 11), (4 ** 3) % 11))
    print("Polynomial Multiply:{}[{}]".format(mult(2, 236), "111011000"))
    print("Polynomial Multiply:{}[{}]".format(mult(0x03, 0xCE, True), "111011000"))
    print("Polynomial Division: {}[{}]".format(
        binary_devision(int("111011000", base=2), int("100011011", base=2), verbose=True), "11000011"))
