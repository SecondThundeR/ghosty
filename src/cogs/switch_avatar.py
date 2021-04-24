import asyncio
from datetime import timedelta
from src.utils.timedelta_formatting import format_timedelta
from src.utils.avatar_changer import get_avatar_bytes


DELAY_TIME = 5


async def switch_avatar(msg, client):
    """Change avatar of bot via command.

    Parameters:
        msg (discord.message.Message): Execute send to channel function
        client (discord.Client): Execute avatar change function
    
    """
    avatar_data = get_avatar_bytes()
    if isinstance(avatar_data, int):
        time_string = format_timedelta(timedelta(seconds=avatar_data))
        await msg.channel.send('Пока что нельзя сменить аватарку. '
                               f'Попробуйте через **{time_string}**',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
    else:
        await client.user.edit(avatar=avatar_data)
        await msg.channel.send('Аватарка успешно изменена!',
                               delete_after=DELAY_TIME)
        await asyncio.sleep(DELAY_TIME)
        await msg.delete()
