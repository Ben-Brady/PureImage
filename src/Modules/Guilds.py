from Modules import Reposts, Logger

import json
import random
import sqlite3

Log = Logger.Get("Guilds")
Store = "./Data/Database.db"
SettingsStore = "./Data/Settings.json"
conn = sqlite3.connect(Store)
Guilds = {}
MaxCache = 250


class Guild:
    rEnabled = bool
    rDelete = bool
    rThreshold = int
    rChannels = list
    rTimeout = int

    Messages = dict

    def __init__(self, ID):
        Log.debug(f"Guild {ID} retrieved")
        self.ID = ID
        with conn:
            Settings = conn.execute(
                "Select SETTINGS from GUILDS where ID = ?",
                (self.ID,),).fetchone()

        if Settings:
            self.LoadJSON(Settings[0])
        else:
            with open(SettingsStore) as fObj:
                self.LoadJSON(fObj.read())
            with conn:
                conn.execute(
                    "Insert into GUILDS values(?,?);",
                    (self.ID, self.SettingJSON)
                )

    @property
    def SettingJSON(self) -> str:
        return json.dumps(self.Settings, indent=4, sort_keys=True)

    @property
    def Settings(self) -> dict:
        return {
            "Reposts": {
                "Enabled": self.rEnabled,
                "Channels": self.rChannels,
                "Delete": self.rDelete,
                "Timeout": self.rTimeout
            },
            "Messages": self.Messages
        }

    def GetMsg(self, msg: str) -> str:
        Messages = self.Messages[msg]
        return random.choice(Messages)

    def Save(self):
        with conn:
            conn.execute(
                "Update GUILDS set SETTINGS = ? where ID = ?;",
                (self.SettingJSON, self.ID)
            )

    def LoadJSON(self, JSON: str):
        JSON = json.loads(JSON)

        assert type(JSON["Reposts"]["Enabled"]) == bool
        assert type(JSON["Reposts"]["Channels"]) == list
        assert type(JSON["Reposts"]["Delete"]) == bool
        assert type(JSON["Reposts"]["Timeout"]) == int
        
        assert type(JSON["Messages"]["rDetect"]) == list

        for x in JSON["Reposts"]["Channels"]:
            assert type(x) == int
        for x in JSON["Messages"]["rDetect"]:
            assert type(x) == str

        self.rEnabled = JSON["Reposts"]["Enabled"]
        self.rChannels = JSON["Reposts"]["Channels"]
        self.rDelete = JSON["Reposts"]["Delete"]
        self.rTimeout = JSON["Reposts"]["Timeout"]

        self.Messages = {
            "rDetect": JSON["Messages"]["rDetect"]
        }
        self.Save()


def Get(ID: int) -> Guild:
    if len(Guilds) > MaxCache:
        Guilds.popitem()
    if ID not in Guilds:
        Guilds[ID] = Guild(ID)
    return Guilds[ID]


def Check(ID: int) -> Guild:
    with conn:
        Settings = conn.execute(
            "Select SETTINGS from SERVERS where ID = ?",
            (ID,),)

    return len(Settings.fetchall()) == 1
