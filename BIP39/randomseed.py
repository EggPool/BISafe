"""
Extracts some entropy, generates 12 words BIP39 mnemonic

Test impl for html wallet and js side crypto.
"""

import hashlib
import json
from Crypto import Random
from mnemonic import Mnemonic
from binascii import hexlify, unhexlify

__version__ = '0.0.1'


def get_entropy():
    """
    Would need improvements to entropy sources to be used IRL. Same as current wallet (only system RNG)
    """

    # Simulates the entropy pool filled by the js wallet.
    pool = Random.get_random_bytes(256)  # bytearray, 256 bytes
    # get the pool hash
    hash = hashlib.sha256(pool).hexdigest()
    # Keep only 128 first bits of the hash as entropy source
    entropy = unhexlify(hash[:32])
    return entropy


def entropy_to_twelve(entropy):
    """
    Entropy is a byte array here, not the hex form
    """
    m = Mnemonic('english')
    twelve = m.to_mnemonic(entropy)
    return twelve


def create_vectors():
    vectors = []
    for i in range(10):
        entropy = get_entropy()
        twelve = entropy_to_twelve(entropy)
        vectors.append({"index": i, "entropy":hexlify(entropy).decode(), "twelvewords": twelve})
    with open("seeds2.json", 'w') as f:
        json.dump(vectors, f)


if __name__ == "__main__":
    """
    entropy = get_entropy()
    twelve = entropy_to_twelve(entropy)
    print(twelve)
    """
    create_vectors()
