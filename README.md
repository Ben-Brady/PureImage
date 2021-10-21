# PureImage

## QuickStart

### Invite the Bot

First, click this [link](https://discord.com/oauth2/authorize?client_id=856451426267299863&scope=bot) and select the desired server from the drop down.

### Load up some settings

The bot handles settings through a settings.json file, this handles options such as what channels the bot is active on. Due to this, the bot won't work when you first invite it and you will have to set it up. The instructions will be messaged to the server owner when you invite the bot, these instructions can be found in the QuickStart.md file.

## Repost Filter

By creating a Perceptual Image Hash of every image posted in the selected channels and comparing against the hashes of already posted images, the bot can detect when an image is too similar to a past image and take action based on your settings. Using a perceptual hash prevents lower quality versions of the same image not being detected. Sadly due to performance reasons, images will be skipped if they're larger than 10MegaPixels or 4MB, the megapixel issue may be removed in the future but the 4MB limit will most likely not.

### Coming Soon

New Features Coming Soon:

- Easier and More Diverse Customization
- Improved Repost Detection by making use of multiple hashes
- Making use of of a new [hash database](https://github.com/AiLECS/pyMIH)
- Improved Video Repost Detect. (Currently using SHA-256)

## Changelog

### [October 19] V1.1

- \[[\#5eb7c3](https://github.com/Ben-Brady/PureImage/commit/5eb7c3395292974a8e6894809cf7c35fa7fe2d89)\]: Moved default settings to Guild.py instead of settings.json
- \[[\#c1e8da](https://github.com/Ben-Brady/PureImage/commit/c1e8da9512ee9902de1b8cdf50e271cec5f471d7)\]: Chnaged Log to bs stored in .ssv to avoid comma injection
- \[[\#091498](https://github.com/Ben-Brady/PureImage/commit/091498c43faa087132042a979a2c90e6070068d8)\]: Rewrote most of Repost Handlers
- \[[\#69c010](https://github.com/Ben-Brady/PureImage/commit/69c010fb5eba6c51f6d96af346fcf2cc9298f259)\]: Changed how Guild's settings are stored
- \[[\#56da4a](https://github.com/Ben-Brady/PureImage/commit/56da4acfe7cc326a8f78e5fc64f078bf87378b81)\]: 56da4ac: Removed matplotlib from dependencies
- \[[\#54ce43](https://github.com/Ben-Brady/PureImage/commit/54ce43f0922c75a1b77c478787e395682666e998)\]: Fixed Vanity Cog not being correctly initiated
- \[[\#1b3d91](https://github.com/Ben-Brady/PureImage/commit/1b3d910f98d35635ad75ffd6d85b3100376824ac)\]: Updated .gitignore
- \[[\#d186e5](https://github.com/Ben-Brady/PureImage/commit/d186e5ddb64e5082f1dbd03e4937b1d07c58837a)\]: Changled logging strucutre to differ between stream and file. Now file logging will be saved as .csv files.
- \[[\#c8f5d5](https://github.com/Ben-Brady/PureImage/commit/c8f5d5686a60bd984b1fc1733c6e5032e51f8b09)\]: Changed file structure and added test data to prepare for automated testing enviroment
- \[[\#26d7f3](https://github.com/Ben-Brady/PureImage/commit/26d7f37b89efbacb13146ccf20885d7a90bf1e0d)\]: Updated .gitignore in an attempt to prevent .env from being updated
- \[[\#fb25e3](https://github.com/Ben-Brady/PureImage/commit/fb25e3ec5c3d98eb32905fdfce408d063d2f6b95)\]: Removed example .env to prevent token leakage when making commits
- \[[\#45a5bf](https://github.com/Ben-Brady/PureImage/commit/45a5bf8f8582e0335846308488a09b55d03c80ac)\]: Added an alert for the bot owner for when a guild invites the bot
- \[[\#ee6f77](https://github.com/Ben-Brady/PureImage/commit/ee6f77e8bd6b36a0941ad587f4ad9801a814cc7d)\]: Setup only creates tables if they don't exist
- \[[\#fe0ae6](https://github.com/Ben-Brady/PureImage/commit/fe0ae665599f3be1ff6a219b6e8f0182baa69943)\]: Removed all references to the porn detector, discord's built-in detection would likely perform much better.
- \[[\#43c5d2](https://github.com/Ben-Brady/PureImage/commit/43c5d2aa04604183f5dd5406995d214a044453f6)\]: Fixed an type on the guilds.Check SQL statement that caused an error, this caused the lack of on join message.

### [July 15] Public Release

- Improved Documentation
- Added a timeout settings for repost cog

### [July 5] Beta 2.1

- Fixed a database issue that prevented the bot from working

### [July 5] Beta 2

- Added Settings Cog, allowing customization from a JSON file
- Moved from local storage to an sqlite3 database.

### [June 28] Beta 1

- Added Repost Cog, allowing for repost detection of duplicate images.

## Hosting the Bot

I'm completely fine with you hosting the bot, even on a large scale. However, just don't claim to have made the bot and make sure you post a link to this repo. After that it's fair game.

In order to host the bot just install the python requirements using the requirements.txt

> pip install -r requirements.txt

Then place your bot token into the .env file

> TOKEN = "BOT_TOKEN"

Then run the setup.py file in order to regenerate the databases and perform other setup.

> python setup.py

Finally, run the main file

> python main.py

## Contributing

If you find any vulnerabilities/problems, just send me an [email](mailto:benbradybusiness@gmail.com) or file an [issue](https://github.com/Ben-Brady/PureImage/issues).

If you wish to develop, set the enviroment variable to increase verbosity and store the database in memory.

> DEPLOYMENT = "TESTING"
