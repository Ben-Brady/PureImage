import os
import logging
import importlib

try:
    coloredlogs = importlib.import_module("coloredlogs")
except:
    coloredlogs = None

LOGFORMAT = "[%(asctime)s] %(levelname)s - %(name)s: %(message)s"
os.environ['COLOREDLOGS_LOG_FORMAT'] = LOGFORMAT

def Get(Name):
    Logger = logging.Logger(Name)
    Logger.setLevel(logging.DEBUG)
    FORMAT = logging.Formatter(LOGFORMAT)

    # ----------- File Handler ----------- #
    FileLogger = logging.FileHandler("./Data/Log.log")
    FileLogger.setLevel(logging.DEBUG)
    FileLogger.setFormatter(FORMAT)
    Logger.addHandler(FileLogger)

    # ---------- Stream Handler ---------- #
    Stream = logging.StreamHandler()
    if os.getenv("DEPLOYMENT") == "TESTING":
        Stream.setLevel(logging.DEBUG)
    else:
        Stream.setLevel(logging.INFO)
    Stream.setFormatter(FORMAT)
    Logger.addHandler(Stream)
    if coloredlogs:
        coloredlogs.install(logger=Logger, level='DEBUG', milliseconds=True)
    Logger.debug("Log Initialised")
    return Logger
