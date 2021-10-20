import hashlib

def Hash(video:bytes):
    return hashlib.sha256(video).digest()

def Check(hash:bytes,other:bytes):
    return hash == other