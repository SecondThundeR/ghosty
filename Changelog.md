# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and starting with changes from 29.11.2020, this bot will have a correct [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 22.05.2021

## Added
- `general`:
  - Implemented checks for custom exceptions
  - Implemented `discord.ext.commands`
  - added more docstrings
  - Changed imports style
  - Switched from `ctx.send` to `ctx.reply` *(In some moments)*
  - Maybe something else where I didn't follow the changelogs...
- `release`: Added `.zip` with cleaned up sources, which are only needed to run the bot
- `avatars`: Added initial 16 avatars for changing them "on the fly"
- `requirements`: Added new requirement - **aiocron**
- `exceptions`: Added initial custom exceptions
- `main`:
  - Checks for cogs specific errors
  - Removal of users from database, if they leave from server
  - Listener for non-commands messages *(Used for Markov chains)*
- `magic_ball`: Initial addition
- `me`: Added tts mode for regular, non-anon, mode
- `russian_roulette`: Added certain variable for message deletion delay
- `markov_chains`: Initial addition *(Beta)*
- `switch_avatars`: Initial addition
- `system`: Added filter for getting full system info *(By default returns reduced info)*
- `uptime`: Added import of `timedelta_formatter` util
- `database`: Added main database class, Added printing error details on database fail
- `files`: Added shutil for full folder removal, Added function for checking folder status *(is empty or not)*, Added display of an error when switching to an exception
- `users`: Added addition/removal of member to/from database, added new function for shipping, Added check for admin/block status of user
- `words_base`:
  - Added missing file closing after writing data
  - Add new warning message for word duplicate, when adding one
- `utils`: Initial addition of file utils:
  - `avatar_changer`
  - `general_scripts`
  - `markov_utils` *(Beta)*
  - `panel_scripts`
  - `timedelta_formatter`
  
## Changed
- `project`: New logo and new name! This project is now called **Ghosty**
- `general`: Changed names of folders and commands files *(For the transition to `discord.ext.commands`)*
- `main`: 
  - Changed imports, docstrings
  - Refactored code
  - Added new commands
  - Limited some functions only for DM
  - Removed `Playing in...` activity
  - Added cron job to change avatar
- `setup`: Renamed to `bot_setup`
- `bot_panel`: Main revamp
  - Move all internal logic to it's own utils
  - Refactored code, updated modules to check
  - Rephrased tip at the end
  - Removed some legacy code for the old database library
- `help`: Updated help message and slightly updated docstrings
- `manage_ignored`: Renamed to `manage_ignore_list`
- `random_ship`:
   - Now returning `ship_text_short` in fast mode
   - Arguments checking was slightly improved
   - Moved data extraction from DB to variables *(Also changed checks with them)*
- `uptime`: Changed alias name of command
- `user_checker`: Switched from some crap in `main` to nice dynamic testing in cog *(Now supports more options!)*
- `DB's`: Updated some tables *(For new commands and features)*
- `database`: 
  - Changed way of interacting with databases with simple query commands, instead of weird parameters
  - Switched from "dynamic" queries to raw ones
  - Switched from database numbers to database names, when executing command
- `files`:
  - Slightly updated code
  - Changed some checks with returning value of `bool()`, simplified functions names
- `users`: Slightly updated code and fixed docstrings
- `words_base`:
  - Simplified functions names
  - Words synced with last changes
  - Added more functions and constants *(Moved from bot_panel.py)*
- `avatar_changer`: Slightly updated code
- `panel_scripts`: Moved check for elements in bot's DB to own function

## Removed
- `general`: Removed 'Beta' from some docstings
- `.gitmodules`: Removed `Webhook-Notifier` submodule
- `main`: Removed `update_member_list()` *(Moved to `main_scripts`)*
- `manage_ignored` and `manage_admins`: Removed local check for DM
- `random_word`: Removed spam check and `modify_data` import
- `rsp`: Removed debug message for purge function
- `uptime`: Removed local `_format_timedelta` function
- `database`: Removed outdated columns to clear, removed unnecessary functions

## Fixed
- `general`: Fixed many things, reported by DeepSource and CodeFactor
- `Changelog`: Fix old link for repository
- `README`: Fixed needed info for bot working and fixed fourth item in `How to use this bot` *(Also fix old link for repo)*
- `LICENSE`: fix year
- `random_ship`:
  - Fixed slicing part of the second username and ship reset
  - Fixed a bug where ship results could not be reset on the next day
- `random_word`: Fixed words updating on database update and function typo
- `russian_roulette`: Fixed wrong function name
- `database`:
  - Fixed checks for data tuple and code for `modify_data` part
  - Fixed wrong table to clear on load
  - Fixed problems with getting single data or multiple from database
  - Fixed *(temporary)* issue of DeepSource - BAN-B608
- `users`: Fixed crash on getting random user from database

## [2.0.1] - 28.02.2021

## Added

- Getting help from DM
- Check for 404 status when getting words from link
- Flag for requirements installing
- Check for missing packages in `setup.py`
- Reset of active ship status on bot startup
- Ignore of IDEA folder *(for future work with PyCharm and etc.)*

## Changed

- Check for DM moved to commands scripts
- Enumerate loops replace with regular ones
- Check for folders and files were merged
- Small change of setup script internals
- Help message text
- Simplify makar text reversing
- Poll's variables moved to dictionary

## Fixed

- Wrong link for word base in setup
- Error of loop with two arrays
- Wrong bold formatting of word
- Typos in README and Changelog files
-

## [2.0.0] - 07.02.2021

## Added

- Docstring for all scripts
- SQL databases for long-term variables
- Setup script for convenient and simple bot setup
- Words were moved to separate .txt files *(Used only for import)*
- Fetching of users and bot on startup
- Fetching of newcomers and adding to database
- Ignore for blocked users
- Dynamic testing without predifined aliases
- New commands `система` and `поиск`
- Сommands for controlling admin and block lists directly from DM
- Custom libraries for simplifying scripts workflow
- Multiplayer for RSP game
- Checks for regular emoji in messages for certain commands
- Checks for unexpected situations

## Changed

- Bot status from 'Online' to 'DND'
- Unlock polls *(You can now run an unlimited number of polls)*
- Addition/deletion of words now part of `random_word.py` and `russian_roulette.py`
- Method of getting random words in `russian_roulette.py` by getting only needed list of words
- All variables from `variables.js` were moved to SQL database
- Help message is now sent to user's DM
- Move getting string of date to `random_ship.py`
- Method of getting outcome of RSP game by comparing with value from dictionary

## Removed

- Heroku files *(Due to unexpected work of bot here and filesystem reset)*
- Strings that were in a separate file `variables.js`
- Custom libs on JS
- JSON arrays
- ESlint configuration file *(Now code checked by DeepSource and Pylint)*

## [1.1.4] - 24.12.2020

## Added

- Ability to pass someone's nickname with `@...` in `хуископ` command
- Messages for some exceptions in mention parsing
- Check for formatted word in array before sending

## Changed

- Message formatting for custom horoscope

## Fixed

- Now passing someone's nickname with `@...` in `шип` command returns normal name
- Start of russian roulette when bullet number is NaN

## [1.1.3] - 15.12.2020

### Added

- `дед` command

### Changed

- Message timeout for 'скип' command extended  to 5 seconds
- Message timeout for 'рандом' command extended to 15 seconds
- Command selector has been moved to a separate function
- Text of help command was updated and decoded from Base64
- Text formatting for JSON array *(Add bold and italic texts)*
- Changed emoji in shipping text

### Fixed

- Wrong behavior of random number function *(More resilient to many wrong argument combination)*
- Fixed no-unsafe-finally in wakeDyno.js
- Skipping "intriguing" text until the result appears
- Incorrect comments in variables.js

## [1.1.2] - 08.12.2020

### Changed

- Question text now showing in all variants of poll messages
- Blocked creation of multiple polls at once
- Synced words array changes

## [1.1.1] - 05.12.2020

### Added

- `анонттс` flag for `йа` command

### Changed

- Double escapes to single in poll message

### Removed

- Comma in russian roulette answer

### Fixed

- Checks for poll votes result

## [1.1.0] - 04.12.2020

### Added

- **[Beta]** Simple poll system *(Can be called via `полл` command)*
- JSONHandlerLib import in main.js
- `влад` command
- `анон` flag for `йа` command

### Changed

- All similar subfunctions were merged
- Random delay time replaced to fixed and has been moved to an external variable
- All text moved to shared variables for localization purposes
- Some if/else statements were changed to switch statement
- Multiple functions and variables names were refactored
- More variables resets after triggering 'скип' flag
- Global code refactor

### Removed

- Async in russian roulette function

### Fixed

- Wrong mention in russian roulette

## [1.0.1] - 29.11.2020

### Removed

- Useless check for arguments length in 'шип' case

## [1.0.0] - 29.11.2020

### Added

- Ignore of package-lock
- Personal library to invoke necessary operations on JSON files
- Blacklist section for further purposes

### Changed

- Start following [semantic versioning](https://semver.org/spec/v2.0.0.html) properly
- Multiple functions and commands was merge into single main commands file
- Timeout for some messages was reduced to 2 seconds
- Timeout for help command was increased to 30 seconds
- Delay time of some modules was increased
- Some functions was renamed
- Many conditions was simplified and refactored
- Some descriptions of modules was rewritten
- Variables for export have been structured and split into several sections
- Uptime command now shows beautifully formatted time
- Names of variables for 'шип' command was renamed
- Text of help command was encoded in Base64
- Most of the text was moved to export variables for easy editing and translation
- Name, version and license was changed in package file

### Removed

- Checks for user to ignore
- Multiple commands and functions was deleted due to move to Heroku *(Some of commands will present in additional branches)*
- Commented code was deleted from main branch

[2.1.0]: https://github.com/SecondThundeR/ghosty/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/SecondThundeR/ghosty/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/SecondThundeR/ghosty/compare/v1.1.4...v2.0.0
[1.1.4]: https://github.com/SecondThundeR/ghosty/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/SecondThundeR/ghosty/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/SecondThundeR/ghosty/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/SecondThundeR/ghosty/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/SecondThundeR/ghosty/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/SecondThundeR/ghosty/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/SecondThundeR/ghosty/compare/v0.9.9...v1.0.0
