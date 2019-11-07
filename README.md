# Basic Secure Communication

This repo contains implementations of the following algorithms:
- linear feedback shift register ([LFSR](https://zipcpu.com/dsp/2017/11/11/lfsr-example.html))
- [RSA](https://hackernoon.com/how-does-rsa-work-f44918df914b) using
  - [chinese decryption](https://crypto.stackexchange.com/questions/2575/chinese-remainder-theorem-and-rsa)
  - [Square-and-Multiply](https://www.practicalnetworking.net/stand-alone/square-and-multiply/)
- Advanced Encryption Standard ([AES](https://de.wikipedia.org/wiki/Advanced_Encryption_Standard))
- [Elgamal Encryption](https://www.geeksforgeeks.org/elgamal-encryption-algorithm/)
- [Deffie Hellman for Elliptic Curves](https://crypto.stackexchange.com/questions/29906/how-does-diffie-hellman-differ-from-elliptic-curve-diffie-hellman) with
- [Elliptic Curve](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication)
- [Cipollas algorithm](https://rosettacode.org/wiki/Cipolla%27s_algorithm)
- [Miller-Rabin Primality Test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)

In [main.py](main.py) is an example how Alice and Bob communicate.
