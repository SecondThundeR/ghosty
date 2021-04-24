import random
import pathlib

def change_profile_picture():
    """Change profile picture of bot to random one.
    
    This function gets random number from 1 to 16 and selects avatar,
    based on this number

    Returns:
        bytes: Bytes of PNG picture
    """
    avatar_path = f"{pathlib.Path().absolute()}/src/avatars/Avatar_{random.randrange(1, 16)}.png"
    f = open(avatar_path, 'rb')
    bytes = f.read()
    f.close()
    return bytes