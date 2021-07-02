from Modules import Logger

import io
from PIL import Image
import imagehash as im

Log = Logger.Get("ImageHash")


def Hash(img: bytes) -> list:
    IMG = Image.open(io.BytesIO(img))
    PHash = im.phash(IMG)

    return bytes.fromhex(str(PHash))


def Distance(Hash: bytes, Other: bytes) -> int:
    # Turn bytes into a bit array
    def Conv(x): return bin(int.from_bytes(x, "big"))

    Total = 0
    for a, b in zip(Conv(Hash), Conv(Other)):
        if a != b:
            Total += 1

    return Total
