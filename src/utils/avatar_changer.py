from random import randrange
from time import time as curr_time
from pathlib import Path
from src.lib.database import get_data, modify_data


CHANGE_COOLDOWN = 900


def get_avatar_bytes():
    """Get bytes from avatar picture.

    This function has built-in check for
    avatar change cooldown

    Returns:
        int: Cooldown time
        bytes: Bytes of PNG
    """
    curr_cooldown = get_data(
        0,
        True,
        'SELECT avatar_cooldown FROM variables',
    ) - int(curr_time())
    if curr_cooldown > 0:
        return int(curr_cooldown)
    else:
        modify_data(
            0, 
            'UPDATE variables SET avatar_cooldown = ?', 
            int(curr_time()) + CHANGE_COOLDOWN
        )
        avatar_path = f"{Path().absolute()}/src/avatars/Avatar_{randrange(1, 16)}.png"
        with open(avatar_path, 'rb') as f:
            bytes = f.read()
        f.close()
        return bytes
