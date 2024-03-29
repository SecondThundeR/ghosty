"""Utils for random shipping.

This utils contains all needed functions to handle some operations.

This file can also be imported as a module and contains the following functions:
    * get_ship_data - parses ship data from DB and return a dictionary
    * format_usernames - parses a list of users into a ship strings
    * lock_shipping - changes variables in DB to lock shipping
"""

import src.lib.database as database
import src.lib.users as users


def get_ship_data():
    """Get ship data from DB and return dictionary.

    Returns:
        dict: Dictionary with ship data
    """
    ship_data = database.get_data(
        "mainDB",
        False,
        "SELECT ship_date, ship_activated, ship_in_active FROM variables",
    )
    return {
        "ship_date": ship_data[0],
        "ship_activated": ship_data[1],
        "ship_in_active": ship_data[2],
    }


async def format_usernames(users_list):
    """Parse a list of users into a ship strings.

    Args:
        users_list (list): List of users to be parsed.

    Returns:
        list: List of formatted ship strings.
    """
    usernames = users.get_members_name([users_list[0], users_list[1]])
    first_sliced_username = usernames[0][:int(len(usernames[0]) / 2)]
    second_sliced_username = usernames[1][int(len(usernames[1]) / 2):]
    final_username = first_sliced_username + second_sliced_username
    ship_text_short = (f"{users_list[0].mention} + {users_list[1].mention},"
                       " #" + final_username)
    ship_text_full = f"{usernames[0]} + {usernames[1]}, #" + final_username
    return [ship_text_short, ship_text_full]


async def lock_shipping():
    """Change variables of shipping in DB."""
    database.modify_data(
        "mainDB",
        "UPDATE variables SET ship_in_active = ?, ship_activated = ?", 1, 1)
    return
