from Modules import Logger

import io
import nude
from PIL import Image

Log = Logger.Get("PornDetector")


def Check(img: bytes):
    if nude.is_nude(io.BytesIO(img)):
        Log.debug("Detected by Nude.js")  # !Debug Only Log Statement
        return 1
    else:
        return 0
