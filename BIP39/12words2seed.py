"""
Takes BIP39 12 words from user, as well as passphrase, generates seed.

Test vectors for html wallet and js side crypto.
"""

import json
from mnemonic import Mnemonic
from binascii import hexlify, unhexlify

__version__ = '0.0.1'


TWELVE_WORDS = ("fire glad trip spider then release square school escape width liar cram",
                "slice broom inhale twist base motor another picnic annual net expand unique",
                "cup demand scrub island name zero nephew hunt nasty share gap industry")


PASS_PHRASES = ('',
                'Bismuth gonna BIS',
                'HxyJwkWSEC+umXv0wbmimeBLPHvo41hN9A88eawovI0VmgnqVkFQ/J158E')



def create_vectors():
    m = Mnemonic('english')
    vectors = []
    i = 0;
    for twelve in TWELVE_WORDS:
        for passphrase in PASS_PHRASES:
            entropy = hexlify(m.to_entropy(twelve)).decode()
            seed = hexlify(m.to_seed(twelve, passphrase)).decode()
            vectors.append({"index": i, "twelvewords": twelve, "passphrase": passphrase, "seed": seed, "entropy":entropy})
            i += 1
    with open("seeds1.json", 'w') as f:
        json.dump(vectors, f)


if __name__ == "__main__":
    create_vectors()
