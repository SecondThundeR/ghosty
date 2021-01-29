"""Initial Setup of secondthunder-py-bot.

This script performs the first initial and further
configuration of the bot through the console.

**Noteworthy:** This script cannot be imported as a module,
as it is a separate file without any use in other files.
Because of it, all functions here are private only
"""


from sys import exit as exit_from_setup
from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import edit_data_in_database
from src.libs.database_handler import remove_data_from_database
from src.libs.files_handler import delete_local_file
from src.libs.words_base_handler import restore_dev_word_base

DB_TABLES = ['bots', 'tokens', 'users', 'word_base', 'variables']
DB_COLUMNS = {
    'bots': 'bots_id',
    'tokens': ['bot_name', 'bot_token'],
    'users': 'users_id',
    'word_base': 'words',
    'variables': ['is_setup_completed', 'current_selected_bot']
}
SETUP_STATUS = get_data_from_database(
    DB_TABLES[4],
    DB_COLUMNS[DB_TABLES[4]][0]
)[0]
WORDS_ARRAY_PATH = 'src/data/words.txt'
WORDS_ARRAY_LINK = 'https://raw.githubusercontent.com/SecondThundeR/' \
                   'secondthunder-js-bot/dev-2.0.0/src/data/words.txt'
WIKI_LINK = 'https://github.com/SecondThundeR/secondthunder-js-bot/' \
            'wiki/FAQ#getting-a-bot-token'
ERROR_MESSAGE = 'Something went wrong. Try again or open an issue on Github'


def _delete_file():
    """Delete local file from data folder."""
    if delete_local_file(WORDS_ARRAY_PATH):
        print(f'File in path \'{WORDS_ARRAY_PATH}\' was deleted successfully')
    else:
        print(f'File in path \'{WORDS_ARRAY_PATH}\' could not be deleted')


def _get_user_input():
    """Get user's input and return it.

    If the user wants to exit the input mode, he needs to enter "Cancel".
    This was done due to the strange behavior of KeyboardInterrupt on Windows.

    Returns:
        str: User's input if all conditions were met
    """
    while True:
        user_input = str(input('> '))
        if user_input != "" and user_input.upper() != "CANCEL":
            if user_input.find("\'") != -1:
                formatted_input = user_input.replace("\'", "''")
                user_input = formatted_input
            return user_input
        if user_input.upper() == "CANCEL" and SETUP_STATUS == 1:
            print(
                'Cancelling input. '
                'Exiting to main menu\n'
                )
            _bot_setup()
        print('It looks like you haven\'t entered anything, '
              'please try again')


def _manage_dev_base():
    """Manage dev's words base.

    This script processes user input and
    selects two scenarios: Deletion of the developer word base
    or importing it
    """
    setup_input = ''
    menu_input = ''
    if SETUP_STATUS == 0:
        print('\nNext step. Do you want to use the developer\'s word base'
              ' or will use it from scratch? (Y/N): ')
        setup_input = _get_user_input()
    else:
        print(
            '\nWhat do you want to do with your word base:'
            '\n1. Import developer\'s word base'
            '\n2. Clear existing word base'
            '\n0. Exit'
        )
        menu_input = _get_user_input()
    if menu_input == '1' or setup_input.lower() == 'y':
        print('\nClearing database and importing '
              'latest developer\'s word base...')
        restore_dev_word_base(
            DB_TABLES[3],
            DB_COLUMNS[DB_TABLES[3]],
            WORDS_ARRAY_LINK,
            WORDS_ARRAY_PATH
        )
        print('The word base was imported successfully')
        if SETUP_STATUS == 1:
            _manage_dev_base()
    elif menu_input == '2':
        remove_data_from_database(DB_TABLES[3])
        print('\nDatabase cleared successfully')
        _manage_dev_base()
    elif setup_input.lower() == 'n':
        print('Deleting developer\'s words base...')
        delete_local_file(WORDS_ARRAY_PATH)
    elif menu_input == '0' and SETUP_STATUS == 1:
        print('')
        _bot_setup()
    else:
        print('It looks like you entered something wrong, '
              'please try again')


def _bot_in_database():
    """Check for bot info existence in database.

    **Noteworthy:** This script has failed attempts counter.
    If it hits 3, script will redirect to main menu.

    Returns:
        str: Bot name if it was found in database
    """
    failed_attempts = 0
    print('Enter the name of the bot')
    while True:
        if failed_attempts == 3:
            print(f'You have entered the bot name '
                  f'incorrectly {failed_attempts} times')
            _bot_setup()
        else:
            bot_name = _get_user_input()
            if is_data_in_database(
                    DB_TABLES[1],
                    DB_COLUMNS[DB_TABLES[1]][0],
                    bot_name
            ):
                print('Bot found in the database!')
                return bot_name
            print('I did not find this name in my database, '
                  'please try to enter the correct name again')
            failed_attempts += 1


def _add_bot_to_database():
    """Add info about bot into the database.

    Current function require user to input bot's name and token to
    add this to the database. If initial setup was completed,
    also redirects to main menu of setup only
    """
    print('\nEnter name of you Discord bot: ')
    bot_name = _get_user_input()
    if SETUP_STATUS == 0:
        print(
            f'Enter your Discord bot token '
            f'(If you don\'t know where to get it, '
            f'go to this page - {WIKI_LINK})')
    else:
        print('Enter your Discord bot token')
    bot_token = _get_user_input()
    add_data_to_database(
        DB_TABLES[1],
        [DB_COLUMNS[DB_TABLES[1]][0], DB_COLUMNS[DB_TABLES[1]][1]],
        [bot_name, bot_token]
    )
    if SETUP_STATUS == 0:
        print('Great, I managed to add this to the database!')
    else:
        print('Great, I managed to add this to the database!\n')
        _bot_setup()


def _delete_bot_from_database():
    """Delete bot from database.

    This script handles bot removal from database and that's it.
    (Did you expect to see rocket launch codes here?)
    """
    print('Enter the name of the bot:')
    bot_name = _bot_in_database()
    if remove_data_from_database(
            DB_TABLES[1],
            DB_COLUMNS[DB_TABLES[1]][0],
            bot_name
    ):
        print('Bot has been deleted from database...\n')
        _bot_setup()


def _manage_setup_status():
    """Edit current setup status.

    This script changes setup status to 0, when it needs to be reseted
    or set to 1, when initial setup was completed
    """
    if SETUP_STATUS == 0 and edit_data_in_database(
        DB_TABLES[4],
        DB_COLUMNS[DB_TABLES[4]][0],
        1
    ):
        print(
            '\nThe initial setup of the bot has been completed.'
            ' To enable bot, run `main.py` script'
            )
    else:
        if edit_data_in_database(DB_TABLES[4], DB_COLUMNS[DB_TABLES[4]][0], 0):
            tables_to_reset = DB_TABLES
            tables_to_reset.pop()
            for item in tables_to_reset:
                remove_data_from_database(item)
            print('\nThe bot\'s settings have been reset. '
                  'Restart the script for initial setup')
            exit_from_setup()


def _bot_settings_manager():
    """Manage bot settings.

    This script allows you to change the internal name
    of the bot in the database, as well as its token
    """
    bot_name = _bot_in_database()
    print(
        '\nWhat do you want to change:'
        '\n1. Name'
        '\n2. Token'
        '\n0. Exit'
    )
    bot_menu = _get_user_input()
    if bot_menu == '1':
        _bot_name_changer(bot_name)
    elif bot_menu == '2':
        _bot_token_changer(bot_name)
    elif bot_menu == '0':
        print('')
        _bot_setup()
    else:
        print('You have chosen something wrong, please try again')
        _bot_settings_manager()


def _bot_name_changer(old_bot_name):
    """Handle bot's name change.

    Parameters:
        old_bot_name (str): Old name of bot to find in database
    """
    print('Enter new bot\'s name:')
    new_bot_name = _get_user_input()
    bot_info = get_data_from_database(
        DB_TABLES[1],
        DB_COLUMNS[DB_TABLES[1]][0],
        old_bot_name
    )
    if edit_data_in_database(
            DB_TABLES[1],
            [DB_COLUMNS[DB_TABLES[1]][0], DB_COLUMNS[DB_TABLES[1]][1]],
            [new_bot_name, bot_info[1]],
            True
    ):
        print('Great, I managed to edit bot\'s name to a new one!\n')
        _bot_setup()


def _bot_token_changer(bot_name):
    """Handle bot's token change.

    Parameters:
        bot_name (str): Bot's name to find in database
    """
    print('Enter new bot\'s token:')
    new_bot_token = _get_user_input()
    if edit_data_in_database(
            DB_TABLES[1],
            [DB_COLUMNS[DB_TABLES[1]][1], DB_COLUMNS[DB_TABLES[1]][0]],
            [new_bot_token, bot_name],
            True
    ):
        print('Great, I managed to edit bot token to a new one!\n')
        _bot_setup()


def _current_bot_selector():
    """Select current bot to run.

    This script allows you to select the desired bot to run
    """
    list_of_bots = get_data_from_database(
        DB_TABLES[1],
        DB_COLUMNS[DB_TABLES[1]][0]
    )
    currently_selected_bot = get_data_from_database(
        DB_TABLES[4],
        DB_COLUMNS[DB_TABLES[4]][1]
    )[0]
    print(f'At the moment, the selected bot is '
          f'{list_of_bots[currently_selected_bot]}')
    print('\nHere are all the bots available to choose from')
    for i, bot_name in enumerate(list_of_bots):
        i += 1
        print(f'{i}. {bot_name}')
    print('0. Exit')
    print('Enter the number of option '
          'you would like to select')
    while True:
        select_bot = _get_user_input()
        if select_bot == '0':
            print('Exiting to main menu\n')
            _bot_setup()
        else:
            try:
                index_of_bot = int(select_bot) - 1
                if index_of_bot in range(len(list_of_bots)):
                    print(f'Great choice! '
                          f'Selecting {list_of_bots[index_of_bot]} as default...\n')
                    if not edit_data_in_database(
                            DB_TABLES[4],
                            DB_COLUMNS[DB_TABLES[4]][1],
                            index_of_bot
                    ):
                        print('Something strange happened! '
                              'Canceling bot selection...\n')
                    _bot_setup()
                else:
                    print('Invalid number of option. Please, try again')
            except ValueError:
                print('It looks like you entered not a number. '
                      'Please, try again')


def _initial_bot_setup():
    """Bot setup, initial phase.

    This script launches 4 main functions: restoration of words base,
    addition of bot to database, managing locally stored words base and
    changing setup status to 1 after successful completion
    """
    _add_bot_to_database()
    _manage_dev_base()
    _manage_setup_status()


def _bot_setup():
    """Bot setup.

    This script allows you to select 6 functions
    for configuring the bot and the database
    """
    print(
        'What do you want to do?'
        '\n1. Change bot\'s settings'
        '\n2. Add new bot in database'
        '\n3. Remove bot from database'
        '\n4. Choose a bot to run'
        '\n5. Edit words database'
        '\n6. Reset bot settings'
        '\n0. Exit'
    )
    menu_input = _get_user_input()
    if menu_input == '1':
        _bot_settings_manager()
    elif menu_input == '2':
        _add_bot_to_database()
    elif menu_input == '3':
        _delete_bot_from_database()
    elif menu_input == '4':
        _current_bot_selector()
    elif menu_input == '5':
        _manage_dev_base()
    elif menu_input == '6':
        _manage_setup_status()
    elif menu_input == '0':
        print('Hope you come back soon! See you later')
        exit_from_setup()
    else:
        print('You have chosen something wrong, please try again\n')
        _bot_setup()


def _bot_setup_init():
    """Select correct bot setup.

    This script checks the current setting status
    and selects the required function to run
    """
    if SETUP_STATUS == 0:
        _initial_bot_setup()
    else:
        _bot_setup()


_bot_setup_init()
