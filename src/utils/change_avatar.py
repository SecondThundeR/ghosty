import random
import pathlib

def change_profile_picture():
    avatar_path = f"{pathlib.Path().absolute()}/src/avatars/Avatar_{random.randrange(1, 16)}.png"
    f = open(avatar_path, 'rb')
    bytes = f.read()
    f.close()
    return bytes