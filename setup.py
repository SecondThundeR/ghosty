"""Setup of secondthunder-py-bot.

This setup performs the first initial and further
configuration of the bot through the console.

**Noteworthy:** This script cannot be imported as a module,
as it is a separate file without any use in other files.
Because of it, all functions here are private only
"""


import sys
from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import edit_data_in_database
from src.libs.database_handler import remove_data_from_database
from src.libs.files_handler import create_local_folder
from src.libs.files_handler import delete_local_folder
from src.libs.words_base_handler import restore_word_base


MAIN_DB_TABLE = 'variables'
MAIN_DB_COLUMNS = ['is_setup_completed', 'current_selected_bot']

CONFIG_DB_TABLE = 'tokens'
CONFIG_DB_COLUMNS = ['bot_name', 'bot_token']

WORDS_DB_TABLES = [
    'main_words_base',
    'roulette_lose_words',
    'roulette_minus_words',
    'roulette_win_words',
    'roulette_zero_words'
    ]
WORDS_DB_COLUMN = 'words'

TABLES_TO_RESET = {
    1: [CONFIG_DB_TABLE],
    2: [
        WORDS_DB_TABLES[0],
        WORDS_DB_TABLES[1],
        WORDS_DB_TABLES[2],
        WORDS_DB_TABLES[3],
        WORDS_DB_TABLES[4]
        ]
    }

SETUP_STATUS = get_data_from_database(
    0,
    MAIN_DB_TABLE,
    MAIN_DB_COLUMNS[0]
    )[0]

FOLDERS_PATH = ['src/words_base', 'src/words_base/roulette_words']

WORDS_PATHS = [
    'src/words_base/words.txt',
    'src/words_base/roulette_words/roulette_lose.txt',
    'src/words_base/roulette_words/roulette_minus.txt',
    'src/words_base/roulette_words/roulette_win.txt',
    'src/words_base/roulette_words/roulette_zero.txt'
    ]

LINKS = [
    'https://raw.githubusercontent.com/SecondThundeR/'
    'secondthunder-py-bot/master/',
    'https://github.com/SecondThundeR/secondthunder-py-bot/'
    'wiki/FAQ#getting-a-bot-token'
    ]


def _get_input():
    """Process input and return it.

    **Noteworthy:** If the user wants to exit the input mode, he can enter "Cancel".
    This was done due to the strange behavior of KeyboardInterrupt on Windows.

    Also this function replace single quote to double quotes for SQL query.
    SQL automatically return this to single quote

    Returns:
        str: User's input if all conditions were met
    """
    while True:
        user_input = str(input('> '))
        if user_input != "" and user_input.upper() != "CANCEL":
            if user_input.find("\'") != -1:
                formatted_input = user_input.replace("\'", "''")
                user_input = formatted_input
            elif user_input.find("'") != -1:
                formatted_input = user_input.replace("'", "''")
                user_input = formatted_input
            return user_input
        if user_input.upper() == "CANCEL" and SETUP_STATUS == 1:
            print('Cancelling input. '
                  'Exiting to main menu\n')
            _bot_setup()
        print('It looks like you haven\'t entered anything, '
              'please try again')


def _restore_dev_base():
    """Restore dev's words base.

    This function initiates downloading and importing words into the database
    and handles folder creation and deletion
    """
    for i, _ in enumerate(FOLDERS_PATH):
        create_local_folder(FOLDERS_PATH[i])
    for i, _ in enumerate(WORDS_DB_TABLES):
        restore_word_base(
                2,
                WORDS_DB_TABLES[i],
                WORDS_DB_COLUMN,
                WORDS_PATHS[i],
                f'{LINKS[0]}{WORDS_PATHS[i]}'
            )
    for i, _ in reversed(list(enumerate(FOLDERS_PATH))):
        delete_local_folder(FOLDERS_PATH[i])


def _delete_words_base():
    """Empty words tables in database.

    This function initiates the deleting all data
    of tables in the database
    """
    for i, _ in enumerate(WORDS_DB_TABLES):
        remove_data_from_database(
            2,
            WORDS_DB_TABLES[i],
        )


def _manage_words_base():
    """Manage words base.

    This function processes user input and selects two scenarios:
    Deletion of the developer word base or importing it
    and clearing words base
    """
    setup_input = ''
    menu_input = ''
    if SETUP_STATUS == 0:
        print('\nNext step. Do you want to use the developer\'s word base'
              ' or will use it from scratch? (Y/N): ')
        setup_input = _get_input()
    else:
        print('\nWhat do you want to do with your word base:'
              '\n1. Import developer\'s word base'
              '\n2. Clear existing word base'
              '\n0. Exit')
        menu_input = _get_input()
    if menu_input == '1' or setup_input.lower() == 'y':
        print('\nClearing database and importing '
              'latest developer\'s word base...')
        _delete_words_base()
        _restore_dev_base()
        print('The word base was imported successfully')
        if SETUP_STATUS == 1:
            _manage_words_base()
    elif menu_input == '2':
        _delete_words_base()
        print('\nDatabase cleared successfully')
        _manage_words_base()
    elif setup_input.lower() == 'n':
        print('Clearing database...')
        _delete_words_base()
    elif menu_input == '0' and SETUP_STATUS == 1:
        print('')
        _bot_setup()
    else:
        print('It looks like you entered something wrong, '
              'please try again')


def _check_for_bot_existence():
    """Check for bot existence in database.

    **Noteworthy:** This function has failed attempts counter.
    If it hits 3, function will redirect to main menu.

    Returns:
        str: Bot name if it was found in database
    """
    failed_attempts = 0
    print('Enter the name of the bot:')
    while True:
        if failed_attempts == 3:
            print('You have entered the bot name '
                  f'incorrectly {failed_attempts} times\n')
            _bot_setup()
        else:
            bot_name = _get_input()
            if is_data_in_database(
                1,
                CONFIG_DB_TABLE,
                CONFIG_DB_COLUMNS[0],
                bot_name
            ):
                print('Bot found in the database!')
                return bot_name
            print('\nI did not find this name in my database, '
                  'please try to enter the correct name again\n')
            failed_attempts += 1


def _add_bot():
    """Add info about bot into the database.

    Current function require user to input bot's name and token to
    add this to the database. If initial setup was completed,
    also redirects to main menu of setup only
    """
    print('\nEnter name of your Discord bot: ')
    bot_name = _get_input()
    if SETUP_STATUS == 0:
        print('Enter your Discord bot token '
              '(If you don\'t know where to get it, '
              f'go to this page - {LINKS[1]})')
    else:
        if is_data_in_database(
            1,
            CONFIG_DB_TABLE,
            CONFIG_DB_COLUMNS[0],
            bot_name
        ):
            print('A bot with the same name is already in the database!'
                  '\nCancel adding ...\n')
            _bot_setup()
        else:
            print('Enter your Discord bot token')
    bot_token = _get_input()
    add_data_to_database(
        1,
        CONFIG_DB_TABLE,
        [CONFIG_DB_COLUMNS[0], CONFIG_DB_COLUMNS[1]],
        [bot_name, bot_token]
    )
    if SETUP_STATUS == 0:
        print('Great, I managed to add this to the database!')
    else:
        print('Great, I managed to add this to the database!\n')
        _bot_setup()


def _delete_bot():
    """Delete bot from database.

    This function handles bot removal from database and that's it.
    (Did you expect to see rocket launch codes here?)
    """
    bot_name = _check_for_bot_existence()
    remove_data_from_database(
        1,
        CONFIG_DB_TABLE,
        CONFIG_DB_COLUMNS[0],
        bot_name
    )
    print('Bot has been deleted from database...\n')
    _bot_setup()


def _manage_setup_status():
    """Edit current setup status.

    This function changes setup status to 0, when it needs to be reseted
    or set to 1, when initial setup was completed
    """
    if SETUP_STATUS == 0:
        edit_data_in_database(
            0,
            MAIN_DB_TABLE,
            MAIN_DB_COLUMNS[0],
            1
        )
        print('\nThe initial setup of the bot has been completed. '
              'To enable bot, run "main.py" script')
        sys.exit()
    else:
        edit_data_in_database(
            0,
            MAIN_DB_TABLE,
            MAIN_DB_COLUMNS[0],
            0
        )
        for db_num in range(1, 3):
            for tables in TABLES_TO_RESET[db_num]:
                remove_data_from_database(db_num, tables)
        print('\nThe bot\'s settings have been reset. '
              'Restart the script for initial setup')
        sys.exit()


def _bot_settings_manager():
    """Manage bot settings.

    This function allows you to change the internal name
    of the bot in the database, as well as its token
    """
    bot_name = _check_for_bot_existence()
    print('\nWhat do you want to change:'
          '\n1. Name'
          '\n2. Token'
          '\n0. Exit')
    bot_menu = _get_input()
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
    new_bot_name = _get_input()
    bot_info = get_data_from_database(
        1,
        CONFIG_DB_TABLE,
        CONFIG_DB_COLUMNS[0],
        old_bot_name
    )
    edit_data_in_database(
        1,
        CONFIG_DB_TABLE,
        [CONFIG_DB_COLUMNS[0], CONFIG_DB_COLUMNS[1]],
        [new_bot_name, bot_info[1]],
        True
    )
    print('Great, I managed to edit bot\'s name to a new one!\n')
    _bot_setup()


def _bot_token_changer(bot_name):
    """Handle bot's token change.

    Parameters:
        bot_name (str): Bot's name to find in database
    """
    print('Enter new bot\'s token:')
    new_bot_token = _get_input()
    edit_data_in_database(
        1,
        CONFIG_DB_TABLE,
        [CONFIG_DB_COLUMNS[0], CONFIG_DB_COLUMNS[1]],
        [bot_name, new_bot_token],
        True
    )
    print('Great, I managed to edit bot token to a new one!\n')
    _bot_setup()


def _main_bot_selector():
    """Select current bot to run.

    This function allows user to select the desired bot to run
    """
    list_of_bots = get_data_from_database(
        1,
        CONFIG_DB_TABLE,
        CONFIG_DB_COLUMNS[0]
    )
    currently_selected_bot = get_data_from_database(
        0,
        MAIN_DB_TABLE,
        MAIN_DB_COLUMNS[1]
    )[0]
    print('At the moment, the selected bot is '
          f'{list_of_bots[currently_selected_bot]}')
    print('\nHere are all the bots available to choose from')
    for i, bot_name in enumerate(list_of_bots):
        i += 1
        print(f'{i}. {bot_name}')
    print('0. Exit')
    print('Enter the number of option '
          'you would like to select')
    while True:
        select_bot = _get_input()
        if select_bot == '0':
            print('Exiting to main menu\n')
            _bot_setup()
        else:
            try:
                index_of_bot = int(select_bot) - 1
                if index_of_bot in range(len(list_of_bots)):
                    print('Great choice! '
                          f'Selecting {list_of_bots[index_of_bot]} as default...\n')
                    edit_data_in_database(
                        0,
                        MAIN_DB_TABLE,
                        MAIN_DB_COLUMNS[1],
                        index_of_bot
                    )
                    _bot_setup()
                else:
                    print('Invalid number of option. Please, try again')
            except ValueError:
                print('It looks like you entered not a number. '
                      'Please, try again')


def _initial_bot_setup():
    """Bot setup, initial phase.

    This function launches 3 main functions: addition of bot to database,
    managing of words base and changing setup status to 1 after successful completion
    """
    _add_bot()
    _manage_words_base()
    _manage_setup_status()


def _bot_setup():
    """Bot setup.

    This function allows user to select 6 functions
    for configuring the bot and the database
    """
    print('What do you want to do?'
          '\n1. Change bot\'s settings'
          '\n2. Add new bot in database'
          '\n3. Remove bot from database'
          '\n4. Choose a bot to run'
          '\n5. Edit words database'
          '\n6. Reset bot settings'
          '\n0. Exit')
    menu_input = _get_input()
    if menu_input == '1':
        _bot_settings_manager()
    elif menu_input == '2':
        _add_bot()
    elif menu_input == '3':
        _delete_bot()
    elif menu_input == '4':
        _main_bot_selector()
    elif menu_input == '5':
        _manage_words_base()
    elif menu_input == '6':
        _manage_setup_status()
    elif menu_input == '0':
        print('Hope you come back soon! See you later')
        sys.exit()
    else:
        print('You have chosen something wrong, please try again\n')
        _bot_setup()


def _bot_setup_init():
    """Select bot setup depending on status.

    This function checks the current setting status
    and selects the required function to run
    """
    if SETUP_STATUS == 0:
        _initial_bot_setup()
    else:
        _bot_setup()


_bot_setup_init()
