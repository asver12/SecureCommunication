import LFSR
from AES import AES
from bitarray import bitarray

if __name__ == "__main__":
    message = "securityisnoeasy"
    startzustand = [1, 1, 1, 1, 0, 0, 0, 0]
    a = bitarray(startzustand)
    start_lfsr = LFSR.lfsr(a, [0, 1, 3, 4])
    key = [next(start_lfsr) for _ in range(120)]
    aes = AES(key)
    aes.encrypt(message)