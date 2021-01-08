"""Initial Setup of secondthunder-py-bot.

This script performs the first initial and further
configuration of the bot through the console.

**Noteworthy:** This script cannot be imported as a module,
as it is a separate file without any use in other files.
Because of it, all functions here are private only
"""


import sys
import requests
from src.libs.database_handler import is_data_in_database
from src.libs.database_handler import add_data_to_database
from src.libs.database_handler import get_data_from_database
from src.libs.database_handler import edit_data_in_database
from src.libs.database_handler import remove_data_from_database
from src.libs.file_handler import import_data_from_local_file
from src.libs.file_handler import check_if_local_file_exists
from src.libs.file_handler import delete_local_file

DB_TABLES = ['bots', 'tokens', 'users', 'words', 'variables']
DB_COLUMNS = {
    'bots': 'bots_id',
    'tokens': ['bot_name', 'bot_token'],
    'users': 'users_id',
    'words': 'words_array',
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


def _restore_words_file():
    """Restore dev's words base from Github.
        
    Returns:
        bool: True if file was downloaded and saved, False otherwise
    """
    if not check_if_local_file_exists(WORDS_ARRAY_PATH):
        r = requests.get(WORDS_ARRAY_LINK)
        with open(WORDS_ARRAY_PATH, 'wb') as f:
            f.write(r.content)
        return True
    return False


def _delete_file():
    """Delete local file from data folder.
        
    Returns:
        bool: True if file was deleted, False otherwise
    """
    delete_status = delete_local_file(WORDS_ARRAY_PATH)
    if delete_status:
        print(f'File in path \'{WORDS_ARRAY_PATH}\' was deleted successfully')
    else:
        print(f'File in path \'{WORDS_ARRAY_PATH}\' could not be deleted')
    return delete_status


def _get_user_input():
    """Get user's input and return it.
    
    **Noteworthy:** This script handles KeyboardInterrupt which
    will redirect to main menu only if initial setup was completed
    
    Returns:
        str: User's input if all conditions were met
    """
    while True:
        try:
            user_input = str(input('> '))
            if user_input != '':
                return user_input
            else:
                print('It looks like you haven\'t entered anything, '
                      'please try again')
        except KeyboardInterrupt:
            if SETUP_STATUS == 0:
                pass
            print('Exiting to main menu\n')
            _bot_setup()


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
            '\nWhat do you to do with your word base:'
            '\n1. Import developer\'s word base'
            '\n2. Clear existing word base'
            '\n0. Exit'
        )
        menu_input = _get_user_input()
    if menu_input == '1' or setup_input.lower() == 'y':
        _restore_words_file()
        print('\nClearing database and importing '
              'latest developer\'s word base...')
        remove_data_from_database(DB_TABLES[3])
        words_array = import_data_from_local_file(WORDS_ARRAY_PATH)
        add_data_to_database(DB_TABLES[3], DB_COLUMNS[DB_TABLES[3]], words_array)
        print('The word base was imported successfully')
        delete_local_file(WORDS_ARRAY_PATH)
        if SETUP_STATUS == 1:
            _manage_dev_base()
    elif menu_input == '2':
        remove_data_from_database(DB_TABLES[3])
        print('\nDatabase cleared successfully')
        _manage_dev_base()
    elif setup_input.lower() == 'n':
        print('Deleting developer\'s words base...')
        delete_local_file(WORDS_ARRAY_PATH)
    elif menu_input == '0':
        if SETUP_STATUS == 1:
            print('')
            _bot_setup()
    else:
        print('It looks like you entered something wrong, '
              'please try again')


def _bot_in_database():
    """Check for bot info existence in database.
    
    **Noteworthy:** This script has failed attempts counter.
    If it hits 3, script will redirect to main menu.
    
    Also this script handles KeyboardInterrupt which
    will redirect to main menu as well
    
    Returns:
        str: Bot name if it was found in database
    """
    failed_attempts = 0
    print('Enter the name of the bot')
    while True:
        try:
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
                else:
                    print('I did not find this name in my database, '
                          'please try to enter the correct name again')
                    failed_attempts += 1
        except KeyboardInterrupt:
            print('Exiting to main menu\n')
            _bot_setup()


def _add_bot_to_database():
    """Add info about bot into the database

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
    if SETUP_STATUS == 0:
        if edit_data_in_database(DB_TABLES[4], DB_COLUMNS[DB_TABLES[4]][0], 1):
            print('\nThe initial setup of the bot has been completed.'
                  ' To enable bot, run `main.py` script')
    else:
        if edit_data_in_database(DB_TABLES[4], DB_COLUMNS[DB_TABLES[4]][0], 0):
            tables_to_reset = DB_TABLES
            tables_to_reset.pop()
            for item in tables_to_reset:
                remove_data_from_database(item)
            print('\nThe bot\'s settings have been reset. '
                  'Restart the script for initial setup')
            sys.exit()


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
    """Selects current bot to run.
    
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
    print(f'\nHere are all the bots available to choose from')
    for i, bot_name in enumerate(list_of_bots):
        i += 1
        print(f'{i}. {bot_name}')
    print('Enter the number of the bot '
          'you want to select to run')
    while True:
        select_bot = _get_user_input()
        index_of_bot = int(select_bot) - 1
        if index_of_bot in range(len(list_of_bots)):
            print(f'Great choice! '
                  f'Selecting {list_of_bots[index_of_bot]} as default...')
            if edit_data_in_database(
                    DB_TABLES[4],
                    DB_COLUMNS[DB_TABLES[4]][1],
                    index_of_bot
            ):
                print('Selected successfully! '
                      'Returning to main menu...\n')
                _bot_setup()
            else:
                print('Something strange happened! '
                      'Canceling bot selection...\n')
                _bot_setup()
        else:
            print('Invalid name of bot. Please, try again')
    pass


def _initial_bot_setup():
    _restore_words_file()
    _add_bot_to_database()
    _manage_dev_base()
    _manage_setup_status()


def _bot_setup():
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
        sys.exit()
    else:
        print('You have chosen something wrong, please try again\n')
        _bot_setup()


def _bot_setup_init():
    if SETUP_STATUS == 0:
        _initial_bot_setup()
    else:
        _bot_setup()


_bot_setup_init()
