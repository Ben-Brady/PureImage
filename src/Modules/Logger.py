import os
import logging
import importlib

try:
    coloredlogs = importlib.import_module("coloredlogs")
except:
    coloredlogs = None

FILEFORMAT = "%(created)f,%(relativeCreated)d,%(levelname)s,%(name)s,%(message)s"
STREAMFORMAT = "[%(asctime)s] %(name)s: %(message)s"

def Get(Name):
    Logger = logging.Logger(Name)
    Logger.setLevel(logging.DEBUG)

    # ----------- File Handler ----------- #
    FileLogger = logging.FileHandler("./Data/Log.csv")
    FileLogger.setLevel(logging.DEBUG)
    FileLogger.setFormatter(logging.Formatter(FILEFORMAT))
    Logger.addHandler(FileLogger)

    # ---------- Stream Handler ---------- #
    Stream = logging.StreamHandler()
    if os.getenv("DEPLOYMENT") == "TESTING":
        Stream.setLevel(logging.DEBUG)
    else:
        Stream.setLevel(logging.INFO)
    os.environ['COLOREDLOGS_LOG_FORMAT'] = STREAMFORMAT
    Stream.setFormatter(logging.Formatter(STREAMFORMAT))
    Logger.addHandler(Stream)
    if coloredlogs:
        coloredlogs.install(logger=Logger, level='DEBUG', milliseconds=True)
    Logger.debug("Log Initialised")
    return Logger
