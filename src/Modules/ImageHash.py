from Modules import Logger

import io
import imagehash as im
from PIL import Image

Image.MAX_IMAGE_PIXELS = 10_000_000
Log = Logger.Get("ImageHash")


def Hash(img: bytes) -> bytes:
    IMG = Image.open(io.BytesIO(img))
    PHash = im.phash(IMG)
    return bytes.fromhex(str(PHash))


def Distance(a: bytes, b: bytes) -> int:
    a_list:list[int] = list(a)
    b_list:list[int] = list(b)
    if len(a_list) != len(b_list):
        raise OverflowError("Byte lengths do not match")

    Difference = 0
    for x, y in zip(a_list, b_list):
        XOR = x ^ y
        for bit in range(8):
            Difference += (XOR >> bit) & 1
    return Difference
