"""'On-fly' avatar changer.

This script allows to change avatar of bot while it's running.
Script gets randomly choosen avatar data to replace current avatar.

This file can also be imported as a module and contains the following functions:
    * get_avatar_bytes - gets bytes from avatar picture
"""


import random
import time
import pathlib
import src.lib.database as database


CHANGE_COOLDOWN = 900


def get_avatar_bytes(avatar_cooldown=None):
    """Get bytes from avatar picture.

    This function has built-in check for
    avatar change cooldown

    Args:
        avatar_cooldown (Union[int, None]): Cooldown for setting new avatar

    Returns:
        Union[int, list[bytes, int]]:
        Current cooldown time or bytes of PNG w/ new cooldown time
    """
    if not avatar_cooldown:
        avatar_cooldown = database.get_data(
            'mainDB',
            True,
            'SELECT avatar_cooldown FROM variables',
        )
    curr_time = int(time.time())
    curr_cooldown = avatar_cooldown - curr_time
    if curr_cooldown > 0:
        return {
            "avatar_cooldown": avatar_cooldown,
            "curr_cooldown": int(curr_cooldown),
            "avatar_bytes": None
        }
    new_avatar_cooldown = curr_time + avatar_cooldown
    database.modify_data(
        'mainDB',
        'UPDATE variables SET avatar_cooldown = ?',
        new_avatar_cooldown
    )
    avatar_path = f"{pathlib.Path().absolute()}/src/avatars/" \
                  f"Avatar_{random.randint(1, 16)}.png"
    with open(avatar_path, 'rb') as f:
        avatar_bytes = f.read()
    f.close()
    return {
        "avatar_cooldown": new_avatar_cooldown,
        "curr_cooldown": None,
        "avatar_bytes": avatar_bytes
    }
