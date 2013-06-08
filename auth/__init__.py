import os
from finder.auth._pbkdf2 import pbkdf2_hex
DB_FMT = "{algorithm}${salt}:{costfactor}${hash}"


def _salt(len=16):
    return os.urandom(len).encode('base_64')


def pbkdf2(key, key_len=12, salt=None):
    iterations = 10000
    key = key.encode('ascii', 'ignore')
    salt = (salt or _salt(64)).encode('ascii', 'ignore')
    dkey = pbkdf2_hex(key, salt, iterations=iterations, keylen=key_len)
    return dkey, salt, DB_FMT.format(
        algorithm='PBKDF2-256',
        salt=salt,
        costfactor=iterations,
        hash=dkey
    )
