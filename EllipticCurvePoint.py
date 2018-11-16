import mathematics

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
                    print("{}: {}+{} = {}".format(i, t, self.elliptic_curve.p, (t + self.elliptic_curve.p)))
                t = t + point
        return t

    def get_inv(self):
        return EllipticCurvePoint(self.x, self.elliptic_curve.p - self.y, self.elliptic_curve)

    def get_y_2(self):
        if self.x != self.elliptic_curve.id:
            return (self.x ** 3 + self.elliptic_curve.a * self.x + self.elliptic_curve.b) % self.elliptic_curve.p
        return None


def get_all_points(elliptic_point, anz=20, verbose=False):
    new_point = elliptic_point
    print(elliptic_point)
    points = [elliptic_point]
    for i in range(anz):
        new_point += elliptic_point
        points.append(new_point)
        if verbose:
            print("Point: {} | y^2: {}".format(new_point, new_point.get_y_2()))
