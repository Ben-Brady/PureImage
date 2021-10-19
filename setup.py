import os
import sqlite3
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

# ------------------------------------ #
#               Databases              #
# ------------------------------------ #

print("\033[1;31m Checking Databases \033[0m")
# Choice = input("Regenerate Databases (y/n):")
DatabaseStore = Path('./Data/Database.db')
if DatabaseStore.exists():
    os.remove(DatabaseStore)

with sqlite3.connect(DatabaseStore) as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS GUILDS(
                ID     INT  PRIMARY KEY NOT NULL,
                Settings    TEXT        NOT NULL
            );""")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS MESSAGES(
                ID          INT  PRIMARY KEY  NOT NULL,
                GuildID     INT               NOT NULL,
                FOREIGN KEY(GuildID)
                    REFERENCES GUILDS(ID)
            );""")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS HASHES(
                MsgID   INT             NOT NULL,
                Hash    BLOB            NOT NULL,
                Type    TEXT            NOT NULL,
                FOREIGN KEY(MsgID)
                    REFERENCES MESSAGES(ID)
            );""")

print("    Databases Regenerated")
