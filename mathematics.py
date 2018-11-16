import random
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


def multiplication_for_cipolla(pair_1, pair_2, w_2, p):
    return [(pair_1[0] * pair_2[0] + w_2 * pair_1[1] * pair_2[1]) % p,
            (pair_1[1] * pair_2[0] + pair_1[0] * pair_2[1]) % p]


def legendre_symbol(a, p):
    """
    compare with "Square Roots from 1; 24, 51, 10 to Dan Shanks from Ezra Brown

    :param a: a relative prime to p
    :param p: prime
    :return:
    """
    ls = a ** ((p - 1) / 2) % p
    return -1 if ls == p - 1 else ls


def cipollas_algorithm(n, p, verbose=False):
    """
    solves a congruence of the form x**2 === n (mod p)

    for more informations check Wikipedia or
    https://rosettacode.org/wiki/Cipolla%27s_algorithm

    :param n: elem of F_p
    :param p: odd prime
    :param verbose:
    :return: x satisfying x**2 = n
    """
    if legendre_symbol(n, p) != 1:
        return None
    a = None
    sample = random.sample(range(p), len(range(p)))
    for i in sample:
        if i != 0:
            if verbose:
                print("{}: {} = {}".format(i, (i ** 2 - n), legendre_symbol(i, p)))
            # Legendre symbol
            if legendre_symbol((i ** 2 - n), p) == -1:
                a = i
                if verbose:
                    print("a = {}".format(a))
                break
    if a:
        w_2 = (a * a - n)
        x1 = [a, 1]
        x2 = multiplication_for_cipolla(x1, x1, w_2, p)
        exponent = int((p + 1) / 2)
        bin_exp = bin(exponent)[2:]  # [::-1]
        if verbose:
            print("Exponent: {} | {}".format(exponent, bin_exp))
        for i in range(1, len(bin_exp)):
            if verbose:
                print("i = {}: {}".format(i, bin_exp[i]))
            if bin_exp[i] == "0":
                x2 = multiplication_for_cipolla(x2, x1, w_2, p)
                x1 = multiplication_for_cipolla(x1, x1, w_2, p)
            else:
                x1 = multiplication_for_cipolla(x1, x2, w_2, p)
                x2 = multiplication_for_cipolla(x2, x2, w_2, p)
        return x1[0], -x1[0] % p
    return None


def miller_rabin_primality_test(prime, security_parameter=11, verbose=False):
    """
    Monte-Carlo-Algorithms which only prime and strong pseudoprime numbers pass
    is not used in practice. Its more likely that something like Baillie-PSW primality test would be chosen

    bit_length  security_parameter
    250         11
    300         9
    400         6
    500         5
    600         3
    ...
    :param prime: prime to test
    :return:
    """
    if prime % 2 == 0:
        return False
    if prime < 6:
        if prime == 2 or prime == 3 or prime == 5:
            return True
        else:
            return False
    u = 1
    r = (prime - 1) // 2
    while r & 1 == 0:
        u += 1
        r //= 2

    if verbose:
        print("{} - 1 = 2^{}*{}".format(prime, u, r))
    for _ in range(security_parameter):
        a = random.randint(1, prime - 3)
        # if verbose:
        #     print("Random Number: {}".format(a))
        z = square_and_multiply_for_modular(a, r, prime)
        if verbose:
            print("{} = {}**{} % {}".format(z, a, r, prime))
        if z != 1 and z != prime - 1:
            for i in range(1, u):
                z = square_and_multiply_for_modular(a, 2, prime)
                if verbose:
                    print("{} = {}**{} % {}".format(z, a, 2, prime))
                if z == 1:
                    return False
            if z != prime - 1:
                return False
    return True


if __name__ == "__main__":
    print("gcd[122,22]:{}, {}, {}".format(*extended_gcd(122, 22)))
    print("gcd[120,23]:{}, {}, {}".format(*extended_gcd(120, 23)))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(5, 4, 12), (5 ** 4) % 12))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(12, 18, 9), (12 ** 18) % 9))
    print("square-and-Multiply: {}[{}]".format(square_and_multiply_for_modular(4, 3, 11), (4 ** 3) % 11))
    print("Polynomial Multiply:{}[{}]".format(mult(2, 236), "111011000"))
    print("Polynomial Multiply:{}[{}]".format(mult(0x03, 0xCE, True), "111011000"))
    print("Polynomial Division: {}[{}]".format(
        binary_division(int("111011000", base=2), int("100011011", base=2), verbose=True), "11000011"))
    print("Miller-Rabin Primality Test: {}[{}]".format(miller_rabin_primality_test(91, 4, True), False))
    print("Miller-Rabin Primality Test: {}[{}]".format(miller_rabin_primality_test(221, 4, True), False))
    print("Miller-Rabin Primality Test: {}[{}]".format(miller_rabin_primality_test(32416190071, 11, True), True))
    print("Cipollas Algorithm: {}[{}]".format(cipollas_algorithm(10, 13), 9))
