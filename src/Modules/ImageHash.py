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
    Hash = list(Hash)
    Other = list(Other)
    if len(Hash) != len(Other):
        raise OverflowError("Byte lengths do not match")

    Difference = 0
    for x, y in zip(Hash, Other):
        XOR = x ^ y
        for bit in range(8):
            Difference += (XOR >> bit) & 1
    return Difference
