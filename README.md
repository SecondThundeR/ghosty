# secondthunder-js-bot (Enchanted Version)

[![DeepScan grade](https://deepscan.io/api/teams/11565/projects/14865/branches/286272/badge/grade.svg)](https://deepscan.io/dashboard#view=project&tid=11565&pid=14865&bid=286272)

This is repository of some random bot for Discord which was created just for fun and for some educational purposes *(Made with Discord.js library)*

<p align="center"><i>At the moment you are on a branch where the functionality of interacting with JSON files is implemented (adding and removing)</i></p>

## How to use this bot

### Local use

0. Install neccesary tools *(Node.js, Any IDE or Code Editor, etc.)*
1. Download or clone this repository
2. Create a Discord Bot on [Discord Developers](https://discord.com/developers/applications) page
3. Grab a token of your bot in 'Bot' section and place it in 'config.json'
4. Run `npm install` to install all libraries for bot
5. Run `npm start` to start a bot
6. After getting a log that bot was logged in, you are good to go

### Heroku use (Not bug-free)

0. Install neccesary tools *(Node.js, Heroku CLI, Any IDE or Code Editor, etc.)*
1. Download or clone this repository
2. Create a Discord Bot on [Discord Developers](https://discord.com/developers/applications) page
3. Grab a token of your bot in 'Bot' section and place it in 'config.json'
4. Create a dyno for your bot on [Heroku](https://dashboard.heroku.com/)
5. Get link of your app and edit a 'DYNO_URL' variable in main.js
6. Pull bot to Heroku and wait for build
7. After getting a log that bot was logged in, you are good to go

> Please keep in mind, if you will you these implementation on Heroku, you can't pull edited JSON from it and after Dyno reset, all changed JSON will be reseted to last commit state

## Changelog

This project has a changelog, which you can find [here](https://github.com/SecondThundeR/secondthunder-js-bot/blob/master/Changelog.md)

## License

This project is licensed under **MIT License**.

For the complete licensing terms, please read [LICENSE](https://github.com/SecondThundeR/secondthunder-js-bot/blob/master/LICENSE) file
