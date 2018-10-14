import LFSR
from AES import AES
from RSA import RSA
from bitarray import bitarray
import helper

def calculation(message, n, e, d, p, q, startzustand = [1, 1, 1, 1, 0, 0, 0, 0], verbose=True):
    ### Alice ###
    ## 1,
    a = bitarray(startzustand)
    start_lfsr_alice = LFSR.lfsr(a, [0, 1, 3, 4])
    key = [next(start_lfsr_alice) for _ in range(120)]
    key = "".join(str(x) for x in startzustand + key)
    if verbose:
        print("--ALICE--------")
        print("LFSR-Key: {}".format(helper.get_split_string_from_list(list(key))))

    ## 2,
    rsa = RSA(p="",q="",n=n,e=e)
    c_1 = rsa.short_public_exponent_encrypt(int("".join(str(i) for i in startzustand), base=2))
    if verbose:
        print("RSA Ciphertext: {}".format(c_1))

    ## 3,
    aes = AES(key)
    c_2 = aes.encrypt(message)
    if verbose:
        print("AES Ciphertext: {}".format(c_2))

    ### Bob ###
    ## 1,
    rsa = RSA(p=p,q=q,e=e, private_key="58:7c:9b:d7:cf:bd:2c:c1:c0:ed:92:c3:52:f8:1b:f1:5e:68:be:b0:b3:7c:cd:b0:4e:37:b4:3f:71:11:5a:31")
    if verbose:
        print("Decryption....")
    bin_str = bin(rsa.chinese_decrypt(c_1))[2:]
    if verbose:
        print("--BOB----------")
        print("RSA Plaintext: {}".format(helper.get_split_string_from_list(list(bin_str))))

    ## 2,
    a = bitarray(bin_str)
    start_lfsr_bob = LFSR.lfsr(a, [0, 1, 3, 4])
    key_bob = [next(start_lfsr_bob) for _ in range(120)]
    key_bob = "".join(str(x) for x in list(bin_str) + key_bob)
    if verbose:
        print("LFSR-Key: {}".format(helper.get_split_string_from_list(list(bin_str))))

    ## 3,
    aes = AES(key_bob)
    corresponding_message = aes.decrypt(c_2)
    if verbose:
        print("Message: {}".format(corresponding_message))
    return message

if __name__ == "__main__":
    n_bob = "00:af:09:83:ad:69:61:1f:8e:5d:a1:20:6f:ce:63:8f:7b:b7:f0:3e:5a:f5:36:67:88:d7:11:26:a9:45:e9:f8:c7"
    e_bob = (2 ** 16) + 1
    d = "58:7c:9b:d7:cf:bd:2c:c1:c0:ed:92:c3:52:f8:1b:f1:5e:68:be:b0:b3:7c:cd:b0:4e:37:b4:3f:71:11:5a:31"
    p = "00:d6:7e:67:25:6f:8a:46:7d:d6:38:31:47:87:02:94:b9"
    q = "00:d0:e8:82:78:f0:21:36:a5:84:d6:9f:14:34:2d:39:7f"
    message = "securityisnoeasy"
    startzustand = [1, 1, 1, 1, 0, 0, 0, 0]
    calculation(message,n_bob,e_bob,d,p,q,startzustand)
