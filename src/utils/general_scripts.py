"""General utils.

This script contains functions used in bot's main script

This file can also be imported as a module and contains the following functions:
    * update_member_list - updates users database on load
    * load_commands - prepares extensions on load
"""


import os
import src.lib.users as users


async def update_member_list(client):
    """Update users database on load.

    **Noteworthy:** Currently adding bot to multiple server can cause
    some DB issues. This will be fixed/implemented in future releases.

    Args:
        client (discord.Client): Client object to fetch members of server
    """
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if not member.bot:
                users.add_member_to_db(member)


async def load_commands(client):
    """Prepare extensions on load.

    Args:
        client (discord.Client): Client object to load extension
    """
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'src.cogs.{filename[:-3]}')
