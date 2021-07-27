# PureImage


### QuickStart

### Invite the Bot

First, click this [link](https://discord.com/oauth2/authorize?client_id=856451426267299863&scope=bot) and select the desired server from the drop down.

### Load up some settings

The bot handles settings through a settings.json file, this handles options such as what channels the bot is active on. Due to this, the bot won't work when you first invite it and you will have to set it up. The instructions will be messaged to the server owner when you invite the bot.

## Features

### Reposts

By creating a PHash of every image posted into the selected channels and comparing it against new images, reposts are able to be detected according to the users settings. The system supports detection of compressed, cropped or even hue-shifted images by making use of multiple hashing algorithms. Sadly, due to performance reasons the bot won't process images larger than 10MP, this will hopefully be fixed when the Porn Filter is added.

### Porn Filter (Coming Soon)

Using the [DeepDanbooru](https://github.com/KichangKim/DeepDanbooru) and [nude.js](https://github.com/pa7/nude.js) projects, PureImage is able detect if a post is considered pornographic and either flag or delete it depending on the server configuration. Additionally, several other porn detection libraries such nudepy are used, the thresholds and settings can all be customised in the settings.

### Coming Soon

New Features Coming Soon:

-   Additional Customisability (Ability to change Messages, Config ...etc.)
-   Porn Filter
-   Better Repost Detection

## Changelog

### [July 15] Public Release

-   Improved Documentation
-   Added a timeout settings for repost cog

### [July 5] Beta 2.1

-   Fixed a database issue that prevented the bot from working

### [July 5] Beta 2

-   Added Settings Cog, allowing cusomisability from a JSON file
-   Moved from local storage to an sqlite3 database.

### [June 28] Beta 1

-   Added Repost Cog, allowing for repost detection of duplicate images.


## Config

Compared to other bots, the server config isn't set and change via commands. Instead it's stored in [JSON](https://en.wikipedia.org/wiki/JSON) which a server owner and message to the bot. This makes it easier for server owners to setup the bot as they don't have to rely on bot commands, instead all options can be changed using a preset. In order to change the bots settings you should send it a [settings.json] file in a guild chat message using the '~set' command.

### JSON

The settings are stored in JSON, this is text based file format that is easy for computer and humans to understand. In order to help editting these settings try using an [Online Editor](https://jsoneditoronline.org/#left=cloud.f69c4ee4a2454ad58eab6effaa5e5e93) that provides syntax highlighting.

### Channel IDs

Many of the commands rely on channel ids, this a unique number that indenifies a discord channel. In order to get these IDs either follow this [Guide](https://support.discord.com/hc/en-us/articles/206346498) or use the '~id' command.

### Settings

#### Reposts

> "Enabled": true/false

If the repost component of the bot

> "Channels": [1,2,3]

The Channels that a bot will check for reposts in, stored in channel ids.

> "Delete": true/false

If the bot

> "Timeout":

#### Porn Filter (Coming Soon)

> "Enabled": false,

If the Porn Filter Component should be enabled

> "NSFWChannels": true/false

If the bot should use the NSFW tag to see what channels it should check.

> "IgnoreChannels": [1,2,3]

the channels that the bot will ignore, for more control.

> "Threshold": 1.0 - 0.0

The threshold used for determining if something is porn, between 1 and 0. 1 is confirmed and 0 is completely safe.

#### Messages

> "rDetect": ["> {AUTHOR},You seem to have posted a repost"],

The messages sent to someone when their repost is detected, randomly chosen. Additionally, the text will can formatted using the format strings below, just surround the word with semicolons: {test}.

Format Text:

    - author
      - The repost message's author's name.
    - AUTHOR
      - Pinging the repost message's author.
    - origin
      - The original author's name.
    - ORIGIN
      - Pinging the original author.

Example:

```python
    "{AUTHOR}, Uh oh a repost you stole from {ORIGIN}"
```


> "pDelete": ["> Hmmmmmmm, You seem to have posted porn. I ask thou... why?"]

The messages sent to someone when their repost is detected, randomly chosen. Additionally, the text will can formatted using the format strings below, just surround the word with semicolons: {test}.

Format Text:

    - author
      - The repost message's author's name.
    - AUTHOR
      - Pinging the repost message's author.
    - certainty
      - The certainty that this image is porn.

Example:

```python
    "{AUTHOR}, Uh oh a repost you stole from {ORIGIN}"
```

## Hosting the Bot

I'm completely fine with you hosting the bot, even on a large scale. However, just don't claim to have made the bot and make sure you post a link to this repo. After that it's fair game.

In order to host the bot just install the python requirements using the requirements.txt

> pip install -r requirements.txt

Then place your bot token into the .env file

> TOKEN = "DISCORD TOKEN GOES HERE"

Then run the setup.py file in order to regenerate the databases.

> python setup.py

Finally, run the main file

> python main.py

## Bug Bounty

If you find any vunerabilites, just send me an email and I'll try to find some way to payback the favour.
