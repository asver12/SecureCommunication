import mathematics
import random

import EllipticCurvePoint as EllipticCurvePoint


class EllipticCurve():
    def __init__(self, a, b, prime):
        """
        All Operations of elliptic Curves

        :param a:
        :param b:
        :param prime:
        """
        if prime <= 3:
            raise ValueError("Prime has to be bigger than 3")
        self.p = prime

        if 4 * a ** 3 + 27 * b ** 2 % prime == 0:
            raise ValueError("4 * a**3 + 27 * b**2 mod p == 0 [{},{},{}]".format(a, b, prime))
        self.a = a
        self.b = b
        self.id = "identity"
        self.e = None

        ### a,b element of Z_p

    def __str__(self):
        """
        :return: (x,y) coordinate
        """
        return "a = {}, b = {}, prime = {}".format(self.a, self.b, self.p)

    def is_point(self, x, y=None, verbose=False):
        if y:
            if x != self.id:
                return y ** 2 % self.p == (x ** 3 + self.a * x + self.b) % self.p
            elif y == self.id:
                return True
        else:
            if x != self.id:
                y_1 = (x ** 3 + self.a * x + self.b) % self.p
                # Check if y is quadratic reciprocity
                y_2 = mathematics.cipollas_algorithm(y_1, self.p, verbose=verbose)
                if y_2 is None:
                    return False
                else:
                    if verbose:
                        print("({0},{1}), ({0},{2})".format(x, *y_2))
                    return True
            else:
                return True
        return False

    def get_point(self, x, verbose=False):
        if self.is_point(x):
            y = (x ** 3 + self.a * x + self.b) % self.p
            y, y_inv = mathematics.cipollas_algorithm(y, self.p, verbose)
            return EllipticCurvePoint(x, y, self), EllipticCurvePoint(x, y_inv, self)
        else:
            return None

    def aprox_number_of_points(self):
        """
        Using Hasse's Theorem

        :return:
        """
        lower_bound = self.p + 1 - 2 * self.p ** (1 / 2)
        upper_bound = self.p + 1 + 2 * self.p ** (1 / 2)
        print("Number of Points: {} <= #E <= {}".format(lower_bound, upper_bound))

    def __find_random_element(self):
        for i in random.sample(range(self.p), self.p):
            x = elliptic_curve.get_point(i)
            if x is not None:
                return x
        return None


if __name__ == "__main__":

    a = 1
    b = 6
    p = 11
    x = 2
    y = 4
    elliptic_curve = EllipticCurve(a, b, p)
    for i in range(p):
        elliptic_curve.is_point(i)
    elliptic_point = EllipticCurvePoint.EllipticCurvePoint(x, y, elliptic_curve)
    EllipticCurvePoint.get_all_points(elliptic_point, verbose=True)
    print(13 * elliptic_point)
