import os
import logging
LOGFORMAT = "[%(asctime)s] %(levelname)s - %(name)s: %(message)s "


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
    Stream.setLevel(logging.INFO)
    Stream.setFormatter(FORMAT)
    Logger.addHandler(Stream)

    Logger.info("Initialised")
    return Logger
