class Alice():
    def __init__(self, private_key, generator_point, elliptic_curve):
        self.elliptic_curve = elliptic_curve
        self.generator_point = generator_point
        self.private_key = private_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def generate_public_key(self):
        return self.private_key*self.generator_point

    def generate_joint_secret(self, received_point):
        return self.private_key*received_point

class Bob():
    def __init__(self, private_key, generator_point, elliptic_curve):
        self.elliptic_curve = elliptic_curve
        self.generator_point = generator_point
        self.private_key = private_key

    def set_private_key(self, private_key):
        self.private_key = private_key

    def generate_public_key(self):
        return self.private_key*self.generator_point

    def generate_joint_secret(self, received_point):
        return self.private_key*received_point

if __name__ == "__main__":
    from EllipticCurve import EllipticCurve
    from EllipticCurvePoint import EllipticCurvePoint

    a = 1
    b = 6
    p = 11
    x = 2
    y = 4
    alice_private_key = 6
    bob_private_key = 2
    elliptic_curve = EllipticCurve(a, b, p)
    generator_point = EllipticCurvePoint(x, y, elliptic_curve)
    print("Generated on Elliptic Curve {} with Generator Point {}".format(elliptic_curve, generator_point))
    alice = Alice(alice_private_key, generator_point, elliptic_curve)
    print("Alice Private_key: {}".format(alice.private_key))
    bob = Bob(bob_private_key, generator_point, elliptic_curve)
    print("Bob Private_key: {}".format(bob.private_key))
    alice_public_key = alice.generate_public_key()
    print("Alice Public_key: {}".format(alice_public_key))
    bob_public_key = bob.generate_public_key()
    print("Bob Public_key: {}".format(bob_public_key))
    alice_secret = alice.generate_joint_secret(bob_public_key)
    bob_secret = bob.generate_joint_secret(alice_public_key)
    print("Shared secret: {} == {} ??".format(alice_secret, bob_secret))