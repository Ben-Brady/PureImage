from Modules import Logger

Log = Logger.Get("dbVersioning")

def _guild_1_0(JSON:dict):
    Log.info("Migrating Guild From 1.0 To 1.1")
    return {
        "Version": "1.1",
        "rEnabled": JSON['Reposts']['Enabled'],
        "rChannels": JSON['Reposts']['Channels'],
        "rDelete": JSON['Reposts']['Delete'],
        "rDetected_msg": JSON['Messages']['rDetect'],
        "rThreshold": 10,
        "rTimeout": JSON['Reposts']['Delete']
        }

def _guild_1_1(JSON:dict):
    return JSON

GuildUpgrades = {
    None:_guild_1_0,
    "1.1":_guild_1_1
}