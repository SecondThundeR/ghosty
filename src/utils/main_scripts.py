"""Bot main script utils.

This script contains functions used in bot's main script

This file can also be imported as a module and contains the following functions:
    * update_member_list - updates users database on load
"""
from src.lib.users import add_member_to_db


async def update_member_list(client):
    """Update users database on load.
    
    Parameters:
        client (discord.Client): Used to fetch members of server
    """
    # TODO: Add blacklist of removed users from database
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            add_member_to_db(member)
