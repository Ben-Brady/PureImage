from Modules import Logger

import io
import imagehash as im
from PIL import Image

Image.MAX_IMAGE_PIXELS = 10_000_000
Log = Logger.Get("ImageHash")


def Hash(img: bytes) -> list:
    IMG = Image.open(io.BytesIO(img))
    PHash = im.phash(IMG)

    return bytes.fromhex(str(PHash))


# TODO: Mew .10 feature: int.count_bits(), use with XOR for hamming distance
def Distance(Hash: bytes, Other: bytes) -> int:
    if len(Hash) != len(Other):
        raise OverflowError("Byte lengths do not match")

    for x, y in zip(Hash, Other):
        Difference = 0
        XOR = x ^ y
        for bit in range(8):
            Difference += (XOR >> bit) & 1
    return Difference
