"""
Low perf pure python arcfour PRNG, for html wallet tests.

See https://pypi.org/project/arc4/ for a fast, C version.
Pycryptodome also has rc4
"""

from binascii import hexlify, unhexlify
from hashlib import sha224
from Crypto.PublicKey import RSA
import sys

LIMIT = 0

class ARC4():

    def __init__(self, key=b''):
        self.S = list(range(256))
        self.i = 0
        self.j = 0
        if key:
            self.init(key)

    def init(self, key):
        j = 0
        keylen = len(key)
        for i in range(256):
            j = (j + self.S[i] + key[i % keylen]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def next(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        return self.S[(self.S[self.j] + self.S[self.i]) % 256]

    def get_random_bytes(self, count):
        global LIMIT
        out = [self.next() for i in range(count)]
        #print("c ", count, out)
        LIMIT +=1
        #if LIMIT > 10:
        #    sys.exit()
        return bytes(out)


if __name__ == "__main__":
    seed = unhexlify("88681642c468e982731a6d08e9e401f2")
    arc4 = ARC4(seed)
    #  In practice, the first 3000 bytes should be removed
    for i in range(3000):
        arc4.next()
    print(arc4.next())
    print(arc4.next())
    print(arc4.next())
    print(arc4.next())

    key = RSA.generate(4096, randfunc=arc4.get_random_bytes)
    # public_key = key.publickey()

    private_key_readable = key.exportKey().decode("utf-8")
    public_key_readable = key.publickey().exportKey().decode("utf-8")
    address = sha224(public_key_readable.encode("utf-8")).hexdigest()
    print(address)
    print(LIMIT)
