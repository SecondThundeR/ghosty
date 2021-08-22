"""Scripts for bot_panel.py.

There are all utils for working with bot_panel.py
For now, all internal logic of configuring bot is handled here

This file can also be imported as a module and contains the following functions:
    * get_user_input - handles user input in console
    * get_curr_setup_status - returns current setup status
    * installed_modules_checker - checks and installs missing modules
    * change_setup_status - changes status of setup
    * import_dev_words - clears and imports dev's word base
    * clear_db_tables - clears words tables in database
    * words_table_manager - manages words table
    * is_bot_in_database - checks if bot in database
    * check_bots_database - checks for elements in bot's database
    * add_bot_config - adds new bot config to database
    * remove_bot_config - removes current bot config from database
    * manage_bot_settings - manages selected bot config
    * change_bot_name - changes selected bot name
    * change_bot_token - changes selected bot token
    * select_bot_config - selects bot to run
    * bot_setup - runs setup phases for bot
"""

import subprocess
import sys
import time

import pkg_resources

import src.lib.database as database
import src.lib.words_base as words_base
from src.lib.exceptions import WordsImportError

MODULES_TO_CHECK = ["discord", "requests", "emoji", "aiocron"]
WIKI_LINK = "https://github.com/SecondThundeR/ghosty/" "wiki/FAQ#getting-a-bot-token"


def get_user_input(text=None):
    """Process input from user.

    **Noteworthy:** If the user wants to exit the input mode, he can enter "Cancel".
    This was done due to the strange behavior of KeyboardInterrupt on Windows.

    Args:
        text (Union[str, None]): Text to print before input
        If nothing was provided, skips printing text

    Returns:
        str: User's input if all conditions were met
    """
    current_status = get_curr_setup_status()

    if text:
        print(text)

    while True:
        current_input = input("> ")
        if current_input or current_input.lower() != "cancel":
            return current_input
        if current_status and current_input.lower() == "cancel":
            print("Cancelling input. " "Exiting to main menu\n")
            break
        print("\nIt looks like you haven't entered anything, "
              "please try again")


def get_curr_setup_status():
    """Get current setup status from database.

    Returns:
        int: Current setup status value
    """
    current_status = database.get_data(
        "mainDB", True, "SELECT is_setup_completed FROM variables")
    return current_status


def installed_modules_checker():
    """Check for currently installed modules and install missing ones.

    This function gets a list of currently installed modules
    and checks if the necessary ones are installed.
    If not, it suggests installing the missing ones
    by running the installation of requirements.txt
    """
    found_packages = []
    pip_version = pkg_resources.get_distribution("pip").version
    packages = list(pkg_resources.working_set)
    for package in packages:
        if package.key in MODULES_TO_CHECK:
            found_packages.append(package.key)
    if len(found_packages) != len(MODULES_TO_CHECK):
        print(found_packages, MODULES_TO_CHECK)
        packages_to_install = " ".join(
            [pkg for pkg in MODULES_TO_CHECK if pkg not in found_packages])
        print(
            f"\nYou are missing some required modules: {packages_to_install}\n"
            "Do you want to install missing modules for correct work of bot? (Y/n)"
        )
        while True:
            user_input = get_user_input()
            if user_input.lower() in ["", "y"]:
                if len(pip_version) > 4:
                    pip_version = pip_version[:-2]
                if float(pip_version) < 21:
                    subprocess.check_call([
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        "requirements.txt",
                        "--upgrade",
                        "--use-feature=2020-resolver",
                    ])
                else:
                    subprocess.check_call([
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        "requirements.txt",
                        "--upgrade",
                    ])
                print("\nRequirements installed!\nContinuing the setup...")
                break
            if user_input.lower() == "n":
                print(
                    "Note that the code may not work "
                    "if you don't install the dependencies. "
                    "To install them manually, "
                    "read blockquote under `How to use this bot` in the README"
                )
                break
            print("You have chosen something wrong, please try again\n")


def change_setup_status():
    """Edit current setup status.

    This function changes setup status to 0, when it needs to be reset
    or set to 1, when initial setup was completed
    """
    current_status = get_curr_setup_status()
    database.modify_data(
        "mainDB",
        "UPDATE variables SET is_setup_completed = ?",
        1 if not current_status else 0,
    )
    if current_status:
        database.reset_bot_tables()
        print("\nThe bot's settings have been reset. "
              "Restart the script for initial setup")
        sys.exit()
    print("The initial setup of the bot has been completed. "
          'To enable bot, run "python main.py"')
    sys.exit()


def import_dev_words():
    """Import developer's word base.

    This function handles clearing database and
    importing latest developer's word base from GitHub
    """
    clear_db_tables()
    print("Importing latest master word base...")
    if not words_base.restore_dev_base():
        raise WordsImportError("Words has been imported with failure.\n"
                               "Seems like link to word base is incorrect, "
                               "so you can open issue on GitHub")
    print("The word base was imported successfully\n")


def clear_db_tables():
    """Clear words tables in database."""
    print("\nClearing database...")
    words_base.clear_words_table()
    print("Database cleared successfully\n")


def words_table_manager():
    """Manage words table.

    This function allows user to import developer word base
    or clearing words table
    """
    current_status = get_curr_setup_status()
    inputs = ["", ""]
    if not current_status:
        inputs[0] = get_user_input("\nDo you want to use the "
                                   "developer's word base "
                                   "or will use it from scratch? (y/N): ")
        if inputs[0].lower() == "y":
            import_dev_words()
        elif inputs[0].lower() in ["", "n"]:
            clear_db_tables()
        else:
            print("\nIt looks like you entered something wrong, "
                  "please try again")
    else:
        print("\nOptions with word base:"
              "\n1. Import developer's word base"
              "\n2. Clear existing word base"
              "\n0. Exit")
        while True:
            inputs[1] = get_user_input("Enter the number of option:")
            if inputs[1].isnumeric():
                inputs[1] = int(inputs[1])
                if inputs[1] == 1:
                    import_dev_words()
                    time.sleep(0.5)
                    break
                if inputs[1] == 2:
                    clear_db_tables()
                    time.sleep(0.5)
                    break
                if inputs[1] == 0:
                    print("")
                    break
            print("\nIt looks like you entered something wrong, "
                  "please try again")


def is_bot_in_database():
    """Check for bot existence in database.

    **Noteworthy:** This function has failed attempts counter.
    If it hits 3, function will redirect to main menu.

    Returns:
        str: Bot name if it was found in database
        None: If hit 3 failed attempts
    """
    failed_attempts = 1
    while True:
        bot_name = get_user_input("\nEnter the name of the bot:")
        if database.get_data("confDB", True,
                             "SELECT bot_name FROM tokens WHERE bot_name = ?",
                             bot_name):
            return bot_name
        if failed_attempts == 3:
            print("You have entered the bot name "
                  f"incorrectly {failed_attempts} times\n")
            return None
        print("I did not find this name in my database, "
              "please try to enter the correct name again")
        failed_attempts += 1


def check_bots_database():
    """Check for elements in bot's database.

    Returns:
        int: Size of list if there is any elements
        None: If table is empty
    """
    db_status = database.get_data("confDB", False,
                                  "SELECT bot_name FROM tokens")
    return None if not db_status else len(db_status)


def add_bot_config():
    """Add bot configuration into the database.

    This function require bot's name and token to add this to the database.
    If initial setup was completed, also redirects to main menu of setup only
    """
    current_status = get_curr_setup_status()
    bot_name = get_user_input("\nEnter name of your Discord bot: ")
    if not current_status:
        print("\nEnter your Discord bot token\n"
              "(If you don't know where to get it, "
              f"go to this page - {WIKI_LINK})")
    else:
        if database.get_data("confDB", True,
                             "SELECT * FROM tokens WHERE bot_name = ?",
                             bot_name):
            print("A bot with the same name is already in the database!"
                  "\nCancel adding ...\n")
        print("\nEnter your Discord bot token")
    while True:
        bot_token = get_user_input()
        if len(bot_token) == 59:
            break
        print("\nIt looks like your token is wrong.\n"
              "It must be 59 characters long "
              f"(Yours is {len(bot_token)} characters long)")
    database.modify_data("confDB", "INSERT INTO tokens VALUES (?, ?)",
                         bot_name, bot_token)
    print(f'\nGreat, I added bot "{bot_name}" to the database!')
    if current_status:
        print("")
    time.sleep(0.5)


def remove_bot_config():
    """Delete bot from database.

    This function handles bot removal from database and that's it.
    (Did you expect to see rocket launch codes here?)
    """
    bots_db_status = check_bots_database()
    if not bots_db_status:
        print("\nThere are no bots in database. "
              "Aborting removing process...\n")
        time.sleep(0.5)
        return
    if bots_db_status == 1:
        print("\nThere is one bot in database.\n"
              "Are you sure you want to remove last bot there? (y/N)")
        while True:
            confirmation = get_user_input().lower()
            if confirmation in ["", "n", "y"]:
                break
            print("You have chosen something wrong, please try again\n")
    if confirmation == "y":
        if not (bot_name := is_bot_in_database()):
            return
        database.modify_data("confDB", "DELETE FROM tokens WHERE bot_name = ?",
                             bot_name)
        print(
            f'\nBot "{bot_name}" has been found and deleted from the database!\n'
        )
    else:
        print("\nSkipping deleting bot from database...\n")
    time.sleep(0.5)


def manage_bot_settings():
    """Manage bot settings.

    This function allows you to change the internal name
    of the bot in the database, as well as its token
    """
    if not check_bots_database():
        print("\nThere are no bots in database. " "Exiting...\n")
        time.sleep(0.5)
        return
    if not (bot_name := is_bot_in_database()):
        return
    print(f'\nOptions with "{bot_name}":'
          "\n1. Name change"
          "\n2. Token change"
          "\n0. Exit to main menu")
    while True:
        menu_select = int(get_user_input())
        if menu_select == 1:
            change_bot_name(bot_name)
            break
        if menu_select == 2:
            change_bot_token(bot_name)
            break
        if menu_select == 0:
            print("")
            break
        print("You have chosen something wrong, please try again")
    time.sleep(0.5)


def change_bot_name(bot_name):
    """Handle name changing of bot.

    Args:
        bot_name (str): Current name of bot
    """
    new_bot_name = get_user_input("\nEnter new bot's name:")
    bot_info = database.get_data("confDB", False,
                                 "SELECT * FROM tokens WHERE bot_name = ?",
                                 bot_name)
    database.modify_data(
        "confDB",
        "UPDATE tokens SET bot_name = ?, bot_token = ?",
        new_bot_name,
        bot_info[1],
    )
    print(f'\nGreat, I changed name from "{bot_name}" to "{new_bot_name}"\n')


def change_bot_token(bot_name):
    """Handle token changing of bot.

    Args:
        bot_name (str): Name of bot to modify
    """
    print("\nEnter new bot's token:")
    while True:
        new_bot_token = get_user_input()
        if len(new_bot_token) == 59:
            break
        print("\nIt looks like your token is wrong.\n"
              "It must be 59 characters long "
              f"(Yours is {len(new_bot_token)} characters long)")
    database.modify_data(
        "confDB",
        "UPDATE tokens SET bot_name = ?, bot_token = ?",
        bot_name,
        new_bot_token,
    )
    print(f'\nGreat, I changed token of "{bot_name}" to a new one!\n')


def select_bot_config():
    """Select main bot to run.

    This function allows user to select the desired bot to run
    when main script starts up
    """
    list_of_bots = database.get_data("confDB", False,
                                     "SELECT bot_name FROM tokens")
    curr_selected_bot = database.get_data(
        "mainDB", True, "SELECT current_selected_bot FROM variables")
    bots_count = 0
    if not list_of_bots:
        print(
            "\nIt looks like there are no bots in my list, try adding a new one\n"
        )
    elif len(list_of_bots) == 1:
        print("\nSince you haven't added any more bots, "
              f'your only active bot is "{list_of_bots[curr_selected_bot]}"\n')
    else:
        print("\nAt the moment, the selected bot is "
              f'"{list_of_bots[curr_selected_bot]}"')
        print("Here are all the added bots:")
        for bot_name in list_of_bots:
            bots_count += 1
            print(f"{bots_count}. {bot_name}")
        print("0. Exit")
        while True:
            select_bot = get_user_input("\nEnter the number of option:")
            if select_bot == "0":
                print("\nExiting to main menu\n")
                break
            try:
                index_of_bot = int(select_bot) - 1
                selected_bot = list_of_bots[index_of_bot]
                if index_of_bot in range(len(list_of_bots)):
                    print("\nGreat choice! "
                          f'Selecting "{selected_bot}" as default...\n')
                    database.modify_data(
                        "mainDB",
                        "UPDATE variables SET current_selected_bot = ?",
                        index_of_bot,
                    )
                    break
                print("Invalid number of option. Please, try again")
            except ValueError:
                print("\nIt looks like you entered not a number. "
                      "Please, try again")
    time.sleep(0.5)


def bot_setup():
    """Bot setup, initial phase.

    This function launches 4 main functions: check for installed modules,
    addition of bot to database, managing of words base
    and changing setup status to 1 after successful completion
    """
    installed_modules_checker()
    add_bot_config()
    words_table_manager()
    change_setup_status()
