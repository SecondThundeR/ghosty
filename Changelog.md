# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and starting with changes from 29.11.2020, this bot will have a correct [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 04.12.2020

### Added

- **[Beta]** Simple poll system
- JSONHandlerLib import in main.js
- 'влад' and 'полл' commands
- 'anon' flag for meMessage.js

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
- Cooldowns of some modules was increased
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

[1.1.0]: https://github.com/SecondThundeR/secondthunder-js-bot/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/SecondThundeR/secondthunder-js-bot/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/SecondThundeR/secondthunder-js-bot/compare/v0.9.9...v1.0.0
