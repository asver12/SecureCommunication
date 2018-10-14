from functools import reduce
from bitarray import bitarray
from operator import itemgetter
import helper
def lfsr(startzustand,connections):
    """
    Gibt immer wenn aufgerufen den nächsten Zustand eines LFSR-Gatherts zurück

    :param startzustand: Bitarray oder Array mit Startzustand
    :param connections: Verbindungen die zur Berechnung des nächsten Zustands genutz werden
    :return: nächster Ausgabezustand
    """

    zustand = startzustand
    while True:
        erg = reduce(lambda x,y: x^y,itemgetter(*connections)(zustand))
        zustand = helper.shift(zustand,1)
        zustand[-1] = erg
        yield int(erg)

if __name__ == "__main__":
    startzustand = [1,1,1,1,0,0,0,0]
    a = bitarray(startzustand)
    start_lfsr = lfsr(a,[0,1,3,4])
    # startzustand = [1, 1, 0, 1]
    # a = bitarray(startzustand)
    # start_lfsr = lfsr(a, [0, 3])
    for i in range(80):
        print("{}: {}".format(i,next(start_lfsr)))
