from typing import Dict, List
from Modules import Logger
from Modules.dbVersioning import GuildUpgrades

import json
import random
import sqlite3

MaxCache = 250
DBSTORE = "./Data/Database.db"
SETTINGS_STORE = "./Data/Settings.json"

Log = Logger.Get("Guilds")
conn = sqlite3.connect(DBSTORE)

Guilds = {}

class Guild:
    rEnabled:bool = True
    rDelete:bool = True
    rTimeout:int = 604800
    rThreshold:int = 10
    rChannels:List[int] = [865270701753892896]
    rDetected_msg:List[str] = ["> {AUTHOR},You seem to have posted a repost"]
    
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
            with conn:
                conn.execute(
                    "Insert into GUILDS values(?,?);",
                    (self.ID, self.Settingjson)
                )

    @property
    def Settingjson(self) -> str:
        return json.dumps(self.Settings, indent=4, sort_keys=True)

    @property
    def Settings(self) -> dict:
        return {
            "Version": "1.1",
            "rEnabled": self.rEnabled,
            "rDelete": self.rDelete,
            "rTimeout": self.rTimeout,
            "rThreshold": self.rThreshold,
            "rChannels": self.rChannels,
            "rDetected_msg": self.rDetected_msg
        }

    @property
    def msgRepostDetected(self) -> str:
        return random.choice(self.rDetected_msg)

    def Save(self):
        Log.debug(f"Saving guild {self.ID}'s Settings")
        with conn:
            conn.execute(
                "Update GUILDS set SETTINGS = ? where ID = ?;",
                (self.Settingjson, self.ID)
            )

    def LoadJSON(self, JSON: str):
        TypeLookup = {
            "rEnabled": [bool],
            "rDelete": [bool],
            "rTimeout": [int],
            "rThreshold": [list,str],
            "rChannels": [list,int],
            "rDetected_msg": [list,int]
            }
        
        Log.debug(f"Loading Guild {self.ID} from JSON")
        JSON:dict = json.loads(JSON)
        
        Version = JSON.get("Version",None)
        JSON = GuildUpgrades[Version](JSON)
        
        #! Data Validation Turned Off
        # for key,value in JSON.items():
        #     if isinstance(TypeLookup[key][0], list):
        #         for x in value:
        #             assert isinstance(x,TypeLookup[key][1])
        #     else:
        #         assert isinstance(value,TypeLookup[key][0])

        self.rEnabled = JSON["rEnabled"]
        self.rDelete = JSON["rDelete"]
        self.rTimeout = JSON["rTimeout"]
        self.rThreshold = JSON["rThreshold"]
        self.rChannels = JSON["rChannels"]
        self.rDetected_msg = JSON["rDetected_msg"]

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
