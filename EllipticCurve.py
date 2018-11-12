import mathematics
import random


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

    def is_point(self, x, y=None):
        if y:
            if x != self.id:
                return y ** 2 % self.p == (x ** 3 + self.a * x + self.b) % self.p
            elif y == self.id:
                return True
        else:
            if x != self.id:
                y_1 = (x ** 3 + self.a * x + self.b) % self.p
                # Check if y is quadratic reciprocity
                y_2 = mathematics.cipollas_algorithm(y_1,self.p, verbose=True)
                if y_2 is None:
                    return False
                else:
                    print(x)
                    print("({0},{1}), ({0},{2})".format(x,*y_2))
                    return True
            else:
                return True
        return False

    def number_of_points(self):
        """
        Using Hasse's Theorem

        :return:
        """
        lower_bound = self.p + 1 - 2 * self.p ** (1 / 2)
        upper_bound = self.p + 1 + 2 * self.p ** (1 / 2)
        print("Number of Points: {} <= #E <= {}".format(lower_bound, upper_bound))
        if self.e == None:
            e = 10

    def __find_random_element(self):
        for i in random.sample(range(self.p)):
            pass

    def __baby_step_giant_step(self, start_point):
        m = random.randint(self.p ** (1 / 4), self.p)
        points = []
        l = 1
        q = (self.p + 1)*start_point
        for i in range(1,m + 1):
            points.append(i*start_point)
        k = 1
        found = False
        act_point = q + k*(2*m*start_point)
        while True:
            for i in range(m + 1):
                if (act_point).x == points[i].x:
                    found = True
                    break
            if found:
                break
            act_point += q + 2*m*start_point
            k += 1
        M = q + 1 +2*m*k


    def find_generator_element(self):
        return 0


class EllipticCurvePoint:

    def __init__(self, x, y, elliptic_curve):
        if not elliptic_curve.is_point(x, y):
            raise ValueError("{},{} is not a point".format(x, y))
        self.x = x
        self.y = y
        self.elliptic_curve = elliptic_curve

    def __str__(self):
        """
        :return: (x,y) coordinate
        """
        return "({},{})".format(self.x, self.y)

    # def __radd__(self, other):
    #     """
    #     pointless since
    #     :param other:
    #     :return:
    #     """
    #     return other.__add__(self)

    def __add__(self, other):
        if self.x == self.elliptic_curve.id:
            return other
        if self.y == self.elliptic_curve.id:
            return self
        if self.x == other.x:
            if self.y == other.get_inv().y:
                return EllipticCurvePoint("identity", "identity", self.elliptic_curve)
            if self.y == other.y:
                y_inv = mathematics.extended_gcd(2 * self.y, self.elliptic_curve.p)[1] % self.elliptic_curve.p
                s = y_inv * (3 * self.x ** 2 + self.elliptic_curve.a) % self.elliptic_curve.p
        else:
            x_inv = mathematics.extended_gcd(other.x - self.x, self.elliptic_curve.p)[1] % self.elliptic_curve.p
            s = (other.y - self.y) * x_inv % self.elliptic_curve.p
        x = (s ** 2 - self.x - other.x) % self.elliptic_curve.p
        y = (s * (self.x - x) - self.y) % self.elliptic_curve.p
        return EllipticCurvePoint(x, y, self.elliptic_curve)

    def __mul__(self, other):
        return self.__double_and_add__(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __double_and_add__(self, point, multiplier, verbose=False):
        """
        Maybe better placement possible
        Calculates the multiplication with a integer

        :param point: EllipticCurve Point
        :param multiplier: Integer to multiply
        :param verbose: verbose output
        :return:
        """
        t = point
        bin_exp = bin(multiplier)[2:][::-1]
        if verbose:
            print("--Double and add-------")
            print("{}^{}".format(t, bin_exp))
        for i in range(multiplier.bit_length() - 2, -1, -1):
            if verbose:
                print("{0}: {1}+{1} = {2}".format(i, t, (t + t)))
            t = t + t
            if bin_exp[i] == "1":
                if verbose:
                    print("{}: {}+{} = {}".format(i, t, p, (t + p)))
                t = t + point
        return t

    def get_inv(self):
        return EllipticCurvePoint(self.x, self.elliptic_curve.p - self.y, self.elliptic_curve)

    def get_y_2(self):
        if self.x != self.elliptic_curve.id:
            return (self.x ** 3 + self.elliptic_curve.a * self.x + self.elliptic_curve.b) % self.elliptic_curve.p
        return None


def get_all_points(elliptic_point, anz = 20, verbose=False):
    new_point = elliptic_point
    print(elliptic_point)
    points = [elliptic_point]
    for i in range(anz):
        new_point += elliptic_point
        points.append(new_point)
        if verbose:
            print("Point: {} | y^2: {}".format(new_point, new_point.get_y_2()))


if __name__ == "__main__":
    a = 1
    b = 6
    p = 11
    x = 2
    y = 4
    # a = 2
    # b = 2
    # p = 17
    # x = 5
    # y = 1
    elliptic_curve = EllipticCurve(a, b, p)
    elliptic_curve.number_of_points()
    for i in range(p):
        elliptic_curve.is_point(i)
    elliptic_point = EllipticCurvePoint(x, y, elliptic_curve)
    get_all_points(elliptic_point, verbose=True)
    print(13 * elliptic_point)
