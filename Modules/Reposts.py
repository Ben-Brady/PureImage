from Modules import Logger, ImageHash, Guild

import io
import time
import sqlite3
from functools import wraps


Log = Logger.Get("Resposts[root]")

# ---------- Repost Section ---------- #


class Section:
    def __init__(self, ID: int) -> None:
        if (ID != 856868040246296578):
            breakpoint

        self.ID = ID
        self.Threshold = 5
        self.DB = "Data/Hash.db"
        self.Logger = Logger.Get(f"Resposts[{ID}]")
        self.SetStore(self.DB)

    def Log(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            Args = tuple([a for a in args if type(a) in (str, int)])

            Start = time.time_ns()
            try:
                ReturnValue = func(self, *args, **kwargs)
            except Exception as e:
                self.Logger.debug(f"{func.__name__}{Args} Failed")
                self.Logger.warning(e.__traceback__)
            else:
                Taken = round((time.time_ns() - Start) / 1000000)
                self.Logger.debug(f"{func.__name__}{Args} in {Taken} ms")

                return ReturnValue
        return wrapped

    @Log
    def Add(self, ID: int, Img: io.BytesIO):
        Hash = ImageHash.Hash(Img)
        with sqlite3.connect(self.DB) as conn:
            conn.execute("Insert into PHASHES VALUES(?,?,?,?);",
                         (ID, self.ID, int(time.time()), bytes(Hash)))

    @Log
    def Remove(self, ID):
        with sqlite3.connect(self.DB) as conn:
            conn.execute("Delete from PHASHES where ID = ?", (ID,))

    @Log
    def Get(self, ID):
        with sqlite3.connect(self.DB) as conn:
            return conn.execute("Select * from PHASHES where ID = ?", (ID,))

    @Log
    def Get(self, ID):
        with sqlite3.connect(self.DB) as conn:
            return conn.execute("Select * from PHASHES where ID = ?", (ID,))

    @Log
    def GetAll(self):
        with sqlite3.connect(self.DB) as conn:
            return conn.execute("Select * from PHASHES where SECTID = ?", (self.ID,))

    @Log
    def Check(self, Img: io.BytesIO):
        with sqlite3.connect(self.DB) as conn:
            Hashes = conn.execute(
                "Select ID,HASH from PHASHES where SECTID = ?", (self.ID,))
        NewHash = ImageHash.Hash(Img)

        for ID, Hash in Hashes:
            if ImageHash.Distance(list(Hash), NewHash) < self.Threshold:
                return ID

    def SetStore(self, Store):
        with sqlite3.connect(Store) as conn:
            self.Logger.debug(f"Database Connection Established at '{Store}''")

            Tables = conn.execute("""
                                SELECT
                                    name
                                FROM
                                    sqlite_master
                                WHERE
                                    type ='table' AND
                                    name NOT LIKE 'sqlite_%';
                                """)

            if ('PHASHES',) not in Tables:
                self.Logger.debug(f"Phashes Table Regenerated at [{Store}]")
                conn.execute("""
                            Create table PHASHES(
                                ID      INT  PRIMARY KEY  NOT NULL,
                                SECTID  INT              NOT NULL,
                                TIME    INT               NOT NULL,
                                HASH    BLOB              NOT NULL
                            );""")

        self.DB = Store
