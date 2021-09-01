<div align="center">

<img width="256" height="256" src="assets/logo.gif">

# Ghosty
</div>

This is repository of some random bot for Discord which was created just for fun and for some educational purposes *(Made with Discord.js library)*

## How to use this bot

> TODO: This section will be simplified or moved to FAQ

1. Install Node.js 16.6.0 or higher
2. Create a Discord Bot on [**Discord Developers**](https://discord.com/developers/applications) page
3. Go to `OAuth2` section to get your Client ID
4. Go to `Bot` section to enable all `Privileged Gateway Intents` and take bot's token
5. Run `git clone https://github.com/SecondThundeR/ghosty.git`, `cd ghosty` and `git checkout javascript-madness`
6. Run `npm install` to install all needed dependencies
7. Open `.env` and insert needed data (**GUILD_ID** is needed for development purposes)
8. Run `npm run register` to register slash commands of bot
9. In terminal, run `npm start` to start bot
10. After getting a log that bot was logged in, you are good to go

> Note: `Router.applicationCommands` is registering global commands, which can show up later because of commands caching (More info [**here**](https://discordjs.guide/interactions/registering-slash-commands.html#global-commands))
>
> To test out changes instantly, use `Router.applicationGuildCommands` and insert ID of guild where you will be testing your bot in `.env` file.

## Discussions

This project has a [**GitHub Discussions**](https://github.com/SecondThundeR/ghosty/discussions) turned on. Feel free to ask about this project or give new ideas etc.

## Changelog

To keep track changes of published versions, check out [**releases**](https://github.com/SecondThundeR/ghosty/releases)

Also, you can track changes of new versions [**here**](https://github.com/SecondThundeR/ghosty/projects)

## License

This project is licensed under **MIT License**.

For the complete licensing terms, please read [**LICENSE**](https://github.com/SecondThundeR/ghosty/blob/master/LICENSE) file

## Credits

`Ghost icon` provided by [VKUI](https://github.com/VKCOM/icons). Licensed with [**MIT License**](https://github.com/VKCOM/icons/blob/master/LICENSE)

`Discord.js` provided by [discordjs](https://github.com/discordjs/discord.js). Licensed with [**Apache License 2.0**](https://github.com/discordjs/discord.js/blob/main/LICENSE)
