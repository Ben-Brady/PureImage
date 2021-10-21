# QuickStart

## Config

Compared to other bots, the server config isn't set and change via commands. Instead it's stored in [JSON](https://en.wikipedia.org/wiki/JSON) which a server owner and message to the bot. This makes it easier for server owners to setup the bot as they don't have to rely on bot commands, instead all options can be changed using a preset. In order to change the bots settings you should send it a [settings.json] file in a guild chat message using the '~set' command.

## JSON

The settings are stored in JSON, this is text based file format that is easy for computer and humans to understand. In order to help editing these settings try using an [Online Editor](https://jsoneditoronline.org/#left=cloud.f69c4ee4a2454ad58eab6effaa5e5e93) that provides syntax highlighting.

## Channel IDs

Many of the commands rely on channel ids, this a unique number that identifies a discord channel. In order to get these IDs either follow this [Guide](https://support.discord.com/hc/en-us/articles/206346498) or use the '~id' command.

## Settings

### Reposts

> "rEnabled": true/false

If the repost component of the bot

> "rChannels": [1,2,3]

The Channels that a bot will check for reposts in, stored in channel ids.

> "rDelete": true/false

If the bot should delete reposts instead of just flagging them for people to see

> "rTimeout": 86400

The timeout for people to be able to repost an image in seconds (e.g. 86400 = 60 x 60 x 24 = 1 Day)

> "rThreshold": 10

The similarity between two images for them to be detected as reposts (0-255)

> "rDetected_msg": ["> {AUTHOR},You seem to have posted a repost"]

The messages sent to someone when their repost is detected, randomly chosen. Additionally, the text will can formatted using the format strings below, just surround the word with semicolons:

Format Text:

    - author
      - The repost message's author's name.
    - AUTHOR
      - Pinging the repost message's author.
    - origin
      - The original author's name.
    - ORIGIN
      - Pinging the original author.

Formatting Example

`"{AUTHOR}, Uh oh a repost you stole from {ORIGIN}"`

### Sample

```js
> ~set
{
    "rEnabled": true,
    "rDelete": true,
    "rTimeout": 86400,
    "rThreshold": 10,
    "rChannels": [],
    "rDetected_msg": ["> {AUTHOR},You seem to have posted a repost"]
}
```
