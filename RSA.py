import mathematics
import helper


class RSA:
    def __init__(self, p, q, n=None, e=None, private_key=None):
        """
        Just for example, The regulare case would differ between en- and decryption

        :param p: Primnumber
        :param q: Primnumber
        :param n: public Modular
        :param e: public Exponent
        :param private_key: private Key
        """
        if p and q:
            if isinstance(p, str):
                self.p = helper.hex_to_int(p)
            else:
                self.p = p
            if isinstance(q, str):
                self.q = helper.hex_to_int(q)
            else:
                self.q = q
            # berechne n
            self.n = self.p * self.q
            if n:
                if isinstance(n, str):
                    n = helper.hex_to_int(n)
                self.__check__(self.n, n, "p*q")

            # berechne phi(n)
            self.phi_n = (self.p - 1) * (self.q - 1)
            if e:
                self.e = e
                self.t = self.__check_e__(self.phi_n, e)
            # else:
            # todo::
            # self.e, self.t = mathematics.find_gcd_with_1(n)
            # setze Public-Key
            self.public_key = (self.n, self.e)
            # berechne Private-Key
            self.private_key = self.t % self.phi_n
            if private_key:
                if isinstance(private_key, str):
                    private_key = helper.hex_to_int(private_key)
                self.__check__(self.private_key, private_key, "PrivatKey")
            # encryption with chinese remainder
            self.c_p = mathematics.extended_gcd(self.q, self.p)[1]
            self.c_q = mathematics.extended_gcd(self.p, self.q)[1]
            self.qc_p = self.q * self.c_p
            self.pc_q = self.p * self.c_q
        else:
            if e and n:
                self.p = None
                self.q = None
                self.private_key = None
                self.phi_n = None
                self.e = e
                self.n = helper.hex_to_int(n)
            else:
                raise Exception("No valide basis, ether e and n or p and q are needed!")

    def __check__(self, n, n_t, text="p*q"):
        if n != n_t:
            raise Exception("{}[{}] != {}".format(text, n, n_t))

    def __check_e__(self, n, e):
        g, s, t = mathematics.extended_gcd(n, e)
        if g != 1:
            Exception("gcd of {} and {} != 1".format(n, e))
        return t

    def short_public_exponent_encrypt(self, plaintext, verbose=False):
        return mathematics.square_and_multiply_for_modular(plaintext, self.e, self.n, verbose=verbose)

    def standard_encrypton(self, plaintext):
        return (plaintext ** self.private_key) % self.public_key[0]

    def chinese_decrypt(self, ciphertext, verbose=False):
        """

        :param ciphertext:
        :return:
        """

        x_p = ciphertext % self.p
        x_q = ciphertext % self.q

        d_p = self.private_key % (self.p - 1)
        d_q = self.private_key % (self.q - 1)

        # y_p = (x_p ** d_p) % self.p
        y_p = mathematics.square_and_multiply_for_modular(x_p, d_p, self.p, verbose=verbose)
        # y_q = (x_q ** d_q) % self.q
        y_q = mathematics.square_and_multiply_for_modular(x_q, d_q, self.q, verbose=verbose)

        if verbose:
            print("--chinese--decrypt--")
            print("x_p: {}".format(x_p))
            print("x_q: {}".format(x_q))
            print("d_p: {}".format(d_p))
            print("d_q: {}".format(d_q))
            print("c_p: {}".format(self.c_p))
            print("c_q: {}".format(self.c_q))
            print("y_p: {}".format(y_p))
            print("y_q: {}".format(y_q))

        return (self.qc_p * y_p + self.pc_q * y_q) % self.n

    def standard_decrypt(self, ciphertext):
        """
        can be made faster by paying attention to how to calculate
        eg square-and-multiply-algorithm
        :param ciphertext:
        :param private_key:
        :param public_key:
        :return:
        """
        return (ciphertext ** self.private_key) % self.public_key[0]

    def convert_plaintext(self, plaintext):
        return int("".join([format(ord(x), 'b') for x in plaintext]), 2)

    def convert_cyphertext(self, cyphertext):
        print(cyphertext)
        # bit_string = format(cyphertext, "0{}b".format((cyphertext).bit_length()+(-(cyphertext).bit_length()%8)))
        return cyphertext.to_bytes((cyphertext.bit_length() + 7) // 8, 'big').decode()

    def print_stats(self):
        if self.p:
            print("p: {}".format(self.p))
            print("p^-1: {}".format(self.c_p))
        if self.q:
            print("q: {}".format(self.q))
            print("q^-1: {}".format(self.c_q))
        if self.n:
            print("n: {}".format(self.n))
        if self.phi_n:
            print("Phi: {}".format(self.phi_n))
        if self.e:
            print("e: {}".format(self.e))
        if self.private_key:
            print("Private Key: {}".format(self.private_key))


if __name__ == "__main__":
    # (4, -1)
    # rsa = RSA("00:d6:7e:67:25:6f:8a:46:7d:d6:38:31:47:87:02:94:b9",
    #           "00:d0:e8:82:78:f0:21:36:a5:84:d6:9f:14:34:2d:39:7f",
    #           n="00:af:09:83:ad:69:61:1f:8e:5d:a1:20:6f:ce:63:8f:7b:b7:f0:3e:5a:f5:36:67:88:d7:11:26:a9:45:e9:f8:c7",
    #           e=(2 ** 16) + 1,
    #           private_key="58:7c:9b:d7:cf:bd:2c:c1:c0:ed:92:c3:52:f8:1b:f1:5e:68:be:b0:b3:7c:cd:b0:4e:37:b4:3f:71:11:5a:31")
    # rsa.print_stats()
    # encrypt = rsa.short_public_exponent_encrypt(100011011)
    # print(encrypt)
    # decrypt = rsa.chinese_decrypt(encrypt)
    # print(decrypt)

    rsa = RSA(p=3, q=11, e=3)
    encrypt = rsa.short_public_exponent_encrypt(4)
    print("Encryption")
    print(encrypt)
    decrypt = rsa.chinese_decrypt(encrypt, verbose=True)
    print("Decryption: ")
    print(decrypt)
    print(rsa.standard_decrypt(31))

    rsa = RSA(p=19, q=17, e=5)
    encrypt = rsa.short_public_exponent_encrypt(240)
    print("Encryption")
    print(encrypt)
    print(rsa.standard_encrypton(240))
    decrypt = rsa.chinese_decrypt(encrypt)
    print("Decryption: ")
    print(decrypt)
    print(rsa.standard_decrypt(encrypt))
