import mathematics


class Bob:
    def __init__(self, private_key, prime, primitiv_element):
        self.d = private_key
        self.p = prime
        self.alpha = primitiv_element

    def __square_and_multiply_for_modular__(self, alpha, d):
        return mathematics.square_and_multiply_for_modular(alpha, d, self.p)

    def decrypt(self, message, ephemeral_key, verbose=False):
        k_m = self.__square_and_multiply_for_modular__(ephemeral_key, self.d)
        inverse_k_m = mathematics.extended_gcd(k_m, self.p)[1]
        if verbose:
            print("K_m: {}".format(k_m))
            print("K_m inv : {}".format(inverse_k_m))
        return (inverse_k_m * message) % self.p

    def calc_beta(self):
        return self.__square_and_multiply_for_modular__(self.alpha, self.d)


class Alice:
    def __init__(self, prime, primitiv_element):
        self.p = prime
        self.alpha = primitiv_element

    def __square_and_multiply_for_modular__(self, alpha, d):
        return mathematics.square_and_multiply_for_modular(alpha, d, self.p)

    def encrypt(self, message, i, beta, verbose=False):
        k_e = self.__square_and_multiply_for_modular__(self.alpha, i)
        if verbose:
            print("K_e: {}".format(k_e))
        k_m = self.__square_and_multiply_for_modular__(beta, i)
        if verbose:
            print("K_m: {}".format(k_m))
        return (message * k_m) % self.p, k_e


if __name__ == "__main__":
    message = 33
    p = 467
    alpha = 2
    d = 105
    i = 123
    bob = Bob(d, p, alpha)
    alice = Alice(p, alpha)
    beta = bob.calc_beta()
    print("Beta: {}".format(beta))
    print("Message: {}".format(message))
    encrypted_message = alice.encrypt(message, i, beta, verbose=True)
    print("Encrypted message: {}".format(encrypted_message))
    decrypted_message = bob.decrypt(*encrypted_message, True)
    print("Message: {}".format(decrypted_message))
