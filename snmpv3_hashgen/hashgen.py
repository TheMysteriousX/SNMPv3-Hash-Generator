import hashlib
import string
import secrets

from itertools import repeat
from functools import partial

P_LEN = 32
E_LEN = 16


class Hashgen(object):
    @staticmethod
    def hash(bytes, alg=hashlib.sha1, raw=False):
        digest = alg(bytes).digest()
        return digest if raw else digest.hex()

    @staticmethod
    def expand(substr, target_len):
        reps = target_len // len(substr) + 1  # approximation; worst case: overrun = l + len(s)
        return "".join(list(repeat(substr, reps)))[:target_len]

    @staticmethod
    def kdf(password, alg=None):
        alg = Hashgen.algs["sha1"] if alg is None else alg

        data = Hashgen.expand(password, 1048576).encode("utf-8")
        return alg(data, raw=True)

    @staticmethod
    def random_string(len=P_LEN, alphabet=(string.ascii_letters + string.digits)):
        return "".join(secrets.choice(alphabet) for _ in range(len))

    @staticmethod
    def random_engine(len=E_LEN):
        return secrets.token_hex(len)

    @staticmethod
    def derive_msg(passphrase, engine, alg):
        # Parameter derivation á la rfc3414
        Ku = Hashgen.kdf(passphrase, alg)
        E = bytearray.fromhex(engine)

        return b"".join([Ku, E, Ku])


# Define available hash algorithms
Hashgen.algs = {
    "sha1": partial(Hashgen.hash, alg=hashlib.sha1),
    "md5": partial(Hashgen.hash, alg=hashlib.md5),
    "sha224": partial(Hashgen.hash, alg=hashlib.sha224),
    "sha256": partial(Hashgen.hash, alg=hashlib.sha256),
    "sha384": partial(Hashgen.hash, alg=hashlib.sha384),
    "sha512": partial(Hashgen.hash, alg=hashlib.sha512),
}
