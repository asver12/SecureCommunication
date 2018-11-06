import mathematics


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

        ### a,b element of Z_p

    def __str__(self):
        """
        :return: (x,y) coordinate
        """
        return "a = {}, b = {}, prime = {}".format(self.a, self.b, self.p)

    def is_point(self, x, y):
        if x != self.id:
            return y ** 2 % self.p == (x ** 3 + self.a * x + self.b) % self.p
        elif y == self.id:
            return True
        return False


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

    def get_inv(self):
        return EllipticCurvePoint(self.x, self.elliptic_curve.p - self.y, self.elliptic_curve)

    def get_y_2(self):
        if self.x != self.elliptic_curve.id:
            return (self.x ** 3 + self.elliptic_curve.a * self.x + self.elliptic_curve.b) % self.elliptic_curve.p
        return None

def get_all_points(elliptic_point):
    new_point = elliptic_point
    print(elliptic_point)
    for i in range(20):
        new_point += elliptic_point
        print("Point: {} | y^2: {}".format(new_point,new_point.get_y_2()))


if __name__ == "__main__":
    a = 1
    b = 6
    p = 11
    elliptic_curve = EllipticCurve(a, b, p)
    elliptic_point = EllipticCurvePoint(2, 4, elliptic_curve)
    get_all_points(elliptic_point)
