"""Text version of RSP game.

This cog handles game logic of rock scissors paper.
"""


import discord
import random
import asyncio
import src.lib.database as database
from discord.ext import commands

WIN_VARIANTS = {
    'камень': 'ножницы',
    'бумага': 'камень',
    'ножницы': 'бумага'
}


class RSPGame(commands.Cog):
    """Class to execute text version of RSP game.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        rsp_mode: Selects needed RSP game mode
        join_check: Checks for correct conditions of join command
        choice_check: Checks for correct conditions of answer selection
        purge_messages: Collects and purges all unreleated messages
        rsp_game: Handles main part of RSP game logic (Defining outcome)
        rsp_bot_game: Handles game with bot
        rsp_multi_game: Handles game of two users

    """

    def __init__(self, client):
        """Initialize variables for RSPGame.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.fail_delay = 4
        self.success_delay = 1

    @commands.command(aliases=['цуефа'])
    async def rsp_mode(self, ctx, *args):
        """Execute correct mode of game depending on arguments.

        If arguments aren't provided, executes multiplayer game.
        Otherwise, executes game with bot

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (RSP variants, if playing with bot)
        """
        if not args:
            if database.get_data(
                'mainDB',
                True,
                'SELECT rsp_game_active FROM variables'
            ):
                await ctx.reply('Сессия игры уже запущена, '
                                'чтобы начать новую игру, закончите старую')
            else:
                await self.rsp_multi_game(self, ctx)
        else:
            await self.rsp_bot_game(self, ctx, args[0])

    @staticmethod
    def join_check(ctx):
        """Check for correct conditions of join command.

        Args:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            bool: True if all conditions are met, False otherwise
        """
        test_string = ctx.content.lower()
        test_channel = isinstance(ctx.channel, discord.channel.DMChannel)
        return bool(test_string == 'играть' and not test_channel)

    @staticmethod
    def choice_check(ctx):
        """Check for correct conditions of answer selection.

        Args:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            bool: True, if all conditions are met, False otherwise
        """
        test_string = ctx.content.lower()
        test_channel = isinstance(ctx.channel, discord.channel.DMChannel)
        return bool(test_string in WIN_VARIANTS and test_channel)

    async def purge_messages(self, messages):
        """Collect and delete all messages, that can distract users in channel.

        Args:
            message (list): List with messages to delete
        """
        for message in messages:
            await message.delete()

    @staticmethod
    def rsp_game(first_var, second_var, first_user_id, second_user_id):
        """Get the outcome of the game and return its result.

        This function handles check for winner of RSP
        If no one wins, throw 'Draw'

        Args:
            first_var (str): First player choice
            second_var (str): Second player choice
            first_user_id (int): First player ID to mention
            second_user_id (int): Second player ID to mention

        Returns:
            str: Outcome of the game
            None: If there are some errors
        """
        f_user_mention = f'<@{first_user_id}>'
        s_user_mention = f'<@{second_user_id}>'
        end_text = '**Игра между ' \
                   f'{f_user_mention} и {s_user_mention} ' \
                   'окончена!**\n'
        outcome_text = ''
        if first_var == WIN_VARIANTS[second_var]:
            outcome_text = f'**Результаты:** {second_var}  🤜  {first_var}\n' \
                        f'{s_user_mention} победил!'
        elif second_var == WIN_VARIANTS[first_var]:
            outcome_text = f'**Результаты:** {first_var}  🤜  {second_var}\n' \
                        f'{f_user_mention} победил!'
        else:
            outcome_text = f'**Результаты:** {first_var}  🙏  {second_var}\n' \
                        'И у нас ничья!'
        return end_text + outcome_text

    async def rsp_bot_game(self, ctx, user_choice):
        """Game with bot.

        This function executes random choice of bot and comparing it with
        players choice

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user_choice (str): Player's move variant
        """
        if user_choice not in WIN_VARIANTS:
            await ctx.reply('Похоже вы выбрали что-то не то...')
        else:
            bot_choice = random.choice(list(WIN_VARIANTS))
            await ctx.send(self.rsp_game(
                self, user_choice, bot_choice,
                ctx.author.id, self.client.user.id
            ))

    async def rsp_multi_game(self, ctx):
        """Game with other users of server.

        This function executes game with other users.

        Also, it waits for another user to play,
        and waits for a response from each in turn,
        then displays the outcome of the game

        **Noteworthy:** When game is live, lock other games to be played,
        while current game isn't finished

        Args:
            ctx (commands.context.Context): Context object to execute functions
        """
        database.modify_data(
            'mainDB',
            'UPDATE variables SET rsp_game_active = ?',
            1
        )
        current_channel = ctx.message.channel
        first_user = ctx.author
        users_choice = []
        messages_to_purge = []
        init_msg = await ctx.reply('Вы запустили игру! '
                                   'Второй игрок, напишите "Играть"\n'
                                   '*До автоотмены - 1 минута*')
        messages_to_purge.append(init_msg)
        try:
            s_user_wait = await self.client.wait_for(
                'message',
                timeout=60,
                check=self.join_check
            )
            second_user = s_user_wait.author
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            await init_msg.edit(
                content='Похоже никто не решил сыграть с вами. '
                'Пока что я отменил данную игру'
            )
            await asyncio.sleep(self.fail_delay)
            await self.purge_messages(self, messages_to_purge)
            return
        else:
            if s_user_wait.author.id == first_user.id:
                database.modify_data(
                    'mainDB',
                    'UPDATE variables SET rsp_game_active = ?',
                    0
                )
                f_user_join = await ctx.reply('Вы решили поиграть сам собой, '
                                              'я отменяю данную игру')
                messages_to_purge.append(s_user_wait)
                messages_to_purge.append(f_user_join)
                await asyncio.sleep(self.fail_delay)
                await self.purge_messages(self, messages_to_purge)
                return
        await s_user_wait.delete()
        await init_msg.edit(content='Сейчас идёт игра между '
                                    f'{first_user.mention} и {second_user.mention}')
        try:
            await first_user.send('Ваш вариант *(На ответ 1 минута)*:')
            first_response = await self.client.wait_for(
                'message',
                timeout=30,
                check=self.choice_check
            )
            users_choice.append(first_response.content.lower())
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            f_move_fail = await current_channel.send(f'{first_user.mention} '
                                                     'не успел ответить вовремя. '
                                                     'Игра отменена')
            messages_to_purge.append(f_move_fail)
            await asyncio.sleep(self.fail_delay)
            await self.purge_messages(self, messages_to_purge)
            return
        try:
            await second_user.send('Ваш вариант *(На ответ 1 минута)*:')
            second_response = await self.client.wait_for(
                'message',
                timeout=30,
                check=self.choice_check
            )
            users_choice.append(second_response.content.lower())
        except asyncio.TimeoutError:
            database.modify_data(
                'mainDB',
                'UPDATE variables SET rsp_game_active = ?',
                0
            )
            s_move_fail = await current_channel.send(f'{second_user.mention} '
                                                     'не успел ответить вовремя. '
                                                     'Игра отменена')
            messages_to_purge.append(s_move_fail)
            await asyncio.sleep(self.fail_delay)
            await self.purge_messages(self, messages_to_purge)
            return
        database.modify_data(
            'mainDB',
            'UPDATE variables SET rsp_game_active = ?',
            0
        )
        await current_channel.send(self.rsp_game(
            self, users_choice[0], users_choice[1],
            first_user.id, second_user.id
        ))
        await self.purge_messages(self, messages_to_purge)


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(RSPGame(client))
