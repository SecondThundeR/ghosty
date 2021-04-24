import asyncio
from time import time as curr_time
from datetime import timedelta
from src.lib.database import get_data, modify_data
from src.utils.timedelta_formatting import format_timedelta
from src.utils.avatar_changer import change_profile_picture


DELAY_TIME = 5
CHANGE_COOLDOWN = 1800


async def switch_avatar(msg, client):
    """Change avatar of bot via command.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        client (discord.Client): Execute avatar change function
    
    """
    curr_cooldown = int(curr_time()) - get_data(
        0,
        True,
        'SELECT avatar_cooldown FROM variables',
    )
    # Testing cooldown at 30 minutes for now
    # If Discord API will "ban" avatar changing
    # we need just simply raise the value
    cooldown_diff = CHANGE_COOLDOWN - curr_cooldown
    time_string = format_timedelta(timedelta(seconds=cooldown_diff))
    if curr_cooldown < CHANGE_COOLDOWN:
        await msg.channel.send('Пока что нельзя сменить аватарку. '
                               f'Попробуйте через **{time_string}**',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    else:
        modify_data(0, 'UPDATE variables SET avatar_cooldown = ?', int(curr_time()))
        await client.user.edit(avatar=change_profile_picture())
        await msg.channel.send('Аватарка успешно изменена!',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()