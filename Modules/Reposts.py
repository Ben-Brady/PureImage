from Modules import Logger, ImageHash, VideoHash,Guilds

import time
import sqlite3
from functools import wraps


Log = Logger.Get("Resposts")
Store = "./Data/Database.db"
conn = sqlite3.connect(Store)
RecentMessages = set()


def MeasureSpeed(func):
    def Wrapper(*args,**kwargs):
        reprArgs = []
        for Arg in args:
            if type(Arg) in (str, int):
                reprArgs.append(Arg)
            else:
                reprArgs.append(str(type(Arg)))
        reprArgs = tuple(reprArgs)
        
        Start = time.time_ns()
        try:
            ReturnValue = func(*args, **kwargs)
        except:
            Log.exception(f"Exception in {func.__name__}{reprArgs}:")
        else:
            Taken = round((time.time_ns() - Start) / 1_000_000)
            Log.debug(f"{func.__name__}{reprArgs} in {Taken} ms")
            return ReturnValue

    return Wrapper


@MeasureSpeed
def AddImage(ID: int, guildID: int, image: bytes):
    Hash = ImageHash.Hash(image)
    with conn:
        if ID not in RecentMessages:
            conn.execute(
                "Insert into MESSAGES VALUES(?,?);",
                (ID, guildID))
            RecentMessages.add(ID)
        conn.execute(
            "Insert into HASHES Values(?,?,'image');",
            (ID, Hash))

@MeasureSpeed
def AddVideo(ID: int, guildID: int, video: bytes):
    Hash = VideoHash.Hash(video)
    with conn:
        if ID not in RecentMessages:
            conn.execute(
                "Insert into MESSAGES VALUES(?,?);",
                (ID, guildID))
            RecentMessages.add(ID)
        conn.execute(
            "Insert into HASHES Values(?,?,'video');",
            (ID, Hash))


@MeasureSpeed
def Remove(ID: int):
    with conn:
        conn.execute(
            "Delete from HASHES where MsgID = ?",
            (ID,))


@MeasureSpeed
def CheckImage(guildID, file: bytes):
    Guild = Guilds.Get(guildID)
    NewHash = ImageHash.Hash(file)
    with conn:
        Hashes = conn.execute("""
            select
                MESSAGES.ID,HASHES.Hash
            from
                MESSAGES
            inner join
                HASHES on MESSAGES.ID = HASHES.MsgID
            where
                MESSAGES.GuildID = ? and HASHES.Type = 'image'
        """, (guildID,))

    for MsgID, Hash in Hashes:
        if ImageHash.Distance(list(Hash), NewHash) < Guild.rThreshold:
            return MsgID

@MeasureSpeed
def CheckVideo(guildID, file: bytes):
    NewHash = VideoHash.Hash(file)
    with conn:
        Hashes = conn.execute("""
            Select
                MESSAGES.ID, HASHES.Hash
            from
                MESSAGES inner join HASHES
                    on MESSAGES.ID = HASHES.MsgID
            where
                MESSAGES.GuildID = ? and HASHES.Hash = ? and HASHES.Type = 'video'
        """, (guildID, NewHash))
    Hash = Hashes.fetchone()
    if Hash:
        return Hashes[0]
