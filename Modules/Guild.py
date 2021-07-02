from Modules import Reposts


class _Guild:
    CleanFeed = True
    Reposts = False
    DeletePost = True

    def __init__(self, ID):
        self.ID = ID
        self.Section = Reposts.Section(ID)


class _GuildOrganiser:
    GuildDict = {}

    def __getitem__(self, ID: str):

        ID = str(ID)
        if ID not in self.GuildDict:
            self.GuildDict[ID] = _Guild(ID)

        return self.GuildDict[ID]


Guilds = _GuildOrganiser()
