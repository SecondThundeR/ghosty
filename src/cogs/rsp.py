"""Text version of RSP game.

This cog handles game logic of rock scissors paper.
"""

import asyncio
import random

import discord
from discord.ext import commands

import src.lib.database as database
import src.utils.economy_utils as economy_utils

WIN_VARIANTS = {"камень": "ножницы", "бумага": "камень", "ножницы": "бумага"}


class RSPGame(commands.Cog):
    """Class to execute text version of RSP game.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        rsp_mode: Selects needed RSP game mode
        __rsp_game: Handles main part of RSP game logic (Defining outcome)
        __rsp_bot_game: Handles game with bot
        __rsp_multi_game: Handles game of two users
        __manage_rsp_state: Manages RSP game state
        __purge_messages: Collects and purges all unreleated messages
        __join_check: Checks for correct conditions of join command
        __choice_check: Checks for correct conditions of answer selection

    """

    def __init__(self, client):
        """Initialize variables for RSPGame.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.fail_delay = 3
        self.success_delay = 1

    @commands.command(aliases=["цуефа"])
    async def rsp_mode(self, ctx, *args):
        """Execute correct mode of game depending on arguments.

        If arguments aren't provided, executes multiplayer game.
        Otherwise, executes game with bot

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (RSP variants, if playing with bot)
        """
        if not args:
            if database.get_data("mainDB", True,
                                 "SELECT rsp_game_active FROM variables"):
                await ctx.reply("Сессия игры уже запущена, "
                                "чтобы начать новую игру, закончите старую")
                return
            await self.__rsp_multi_game(ctx)
            return
        if len(args) == 1:
            if args[0].isnumeric():
                await self.__rsp_multi_game(ctx, args[0])
                return
            await self.__rsp_bot_game(ctx, args[0])
            return
        if len(args) == 2:
            if args[1].isnumeric():
                await self.__rsp_bot_game(ctx, args[0], args[1])
                return
            await ctx.reply("Похоже вы передали неверное значение!")
            return

    async def __rsp_game(self, ctx, f_var, s_var, f_user_id, s_user_id, bet_points=None):
        """Get the outcome of the game and return its result.

        This function handles check for winner of RSP
        If no one wins, throw 'Draw'

        Args:
            f_var (str): First player choice
            s_var (str): Second player choice
            f_user_id (int): First player ID
            s_user_id (int): Second player ID
            bet_points (Union[str, None]): Points to bet

        Returns:
            str: Outcome of the game
            None: If there are some errors
        """
        f_user = await ctx.message.guild.fetch_member(f_user_id)
        s_user = await ctx.message.guild.fetch_member(s_user_id)
        if bet_points is not None:
            bet_points = int(bet_points)
            economy_utils.subtract_points(f_user_id, bet_points, True)
            if s_user_id != self.client.user.id:
                economy_utils.subtract_points(s_user_id, bet_points, True)
            end_text = ("**Игра между "
                        f"{f_user.mention} и {s_user.mention} "
                        f"на {bet_points} очков окончена!**\n")
        else:
            end_text = ("**Игра между "
                        f"{f_user.mention} и {s_user.mention} "
                        "окончена!**\n")
        outcome_text = ""
        if f_var == WIN_VARIANTS[s_var]:
            outcome_text = (f"**Результаты:** {s_var}  🤜  {f_var}\n"
                            f"{s_user.mention} победил!")
            if bet_points is not None and s_user_id != self.client.user.id:
                economy_utils.add_points(s_user_id, bet_points * 2, True)
                outcome_text += f" Также победитель получает **{bet_points * 2}** очков!"
        elif s_var == WIN_VARIANTS[f_var]:
            outcome_text = (f"**Результаты:** {f_var}  🤜  {s_var}\n"
                            f"{f_user.mention} победил!")
            if bet_points is not None:
                economy_utils.add_points(f_user_id, bet_points * 2, True)
                outcome_text += f" Также победитель получает **{bet_points * 2}** очков!"
        else:
            outcome_text = (f"**Результаты:** {f_var}  🙏  {s_var}\n"
                            "И у нас ничья!")
            if bet_points is not None:
                if s_user_id != self.client.user.id:
                    outcome_text += f" Все игроки возвращают себе {bet_points} очков!"
                else:
                    outcome_text += f" {f_user.mention} возвращает себе {bet_points} очков!"
                economy_utils.add_points(f_user_id, bet_points, True)
                if s_user_id != self.client.user.id:
                    economy_utils.add_points(s_user_id, bet_points, True)
        return end_text + outcome_text

    async def __rsp_bot_game(self, ctx, user_choice, bet_points=None):
        """Game with bot.

        This function executes random choice of bot and comparing it with
        players choice

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user_choice (str): Player's move variant
            bet_points (Union[str, None]): Points to bet
        """
        if bet_points is not None:
            player_balance = economy_utils.get_account_balance(ctx.author.id)
            if player_balance is None:
                await ctx.reply(
                    "У вас нет аккаунта с очками для ставок!",
                    delete_after=self.fail_delay
                )
                await asyncio.sleep(self.fail_delay)
                await ctx.message.delete()
                return
            if player_balance < int(bet_points):
                await ctx.reply(
                    "У вас недостаточно очков для ставки!",
                    delete_after=self.fail_delay
                )
                await asyncio.sleep(self.fail_delay)
                await ctx.message.delete()
                return
        if user_choice not in WIN_VARIANTS:
            await ctx.reply("Похоже вы выбрали что-то не то...")
        else:
            bot_choice = random.choice(list(WIN_VARIANTS))
            await ctx.send(
                await self.__rsp_game(ctx, user_choice, bot_choice, ctx.author.id,
                                      self.client.user.id, bet_points))

    async def __rsp_multi_game(self, ctx, bet_points=None):
        """Game with other users of server.

        This function executes game with other users.

        Also, it waits for another user to play,
        and waits for a response from each in turn,
        then displays the outcome of the game

        **Noteworthy:** When game is live, lock other games to be played,
        while current game isn't finished

        Args:
            ctx (commands.context.Context): Context object to execute functions
            bet_points (Union[str, None]): Points to bet
        """
        self.__manage_rsp_state(lock_state=True)
        current_channel = ctx.message.channel
        first_user = ctx.author
        users_choice = []
        messages_to_purge = []
        if bet_points is not None:
            f_player_balance = economy_utils.get_account_balance(first_user.id)
            if f_player_balance is None:
                self.__manage_rsp_state(lock_state=False)
                await ctx.reply(
                    "У вас нет аккаунта с очками для ставок!",
                    delete_after=self.fail_delay
                )
                await asyncio.sleep(self.fail_delay)
                await ctx.message.delete()
                return
            if f_player_balance < int(bet_points):
                self.__manage_rsp_state(lock_state=False)
                await ctx.reply(
                    "У вас недостаточно очков для ставки!",
                    delete_after=self.fail_delay
                )
                await asyncio.sleep(self.fail_delay)
                await ctx.message.delete()
                return
        init_msg = await ctx.reply("Вы запустили игру! "
                                   'Второй игрок, напишите "Играть"\n'
                                   "*До автоотмены - 1 минута*")
        messages_to_purge.append(init_msg)
        try:
            s_user_wait = await self.client.wait_for("message",
                                                     timeout=60,
                                                     check=self.__join_check)
            second_user = s_user_wait.author
        except asyncio.TimeoutError:
            self.__manage_rsp_state(lock_state=False)
            await init_msg.edit(
                content="Похоже никто не решил сыграть с вами. "
                "Пока что я отменил данную игру")
            await asyncio.sleep(self.fail_delay)
            await self.__purge_messages(messages_to_purge)
            return
        else:
            if s_user_wait.author.id == first_user.id:
                self.__manage_rsp_state(lock_state=False)
                f_user_join = await ctx.reply("Вы решили поиграть сам собой, "
                                              "я отменяю данную игру")
                messages_to_purge.append(s_user_wait)
                messages_to_purge.append(f_user_join)
                await asyncio.sleep(self.fail_delay)
                await self.__purge_messages(messages_to_purge)
                return
        await s_user_wait.delete()
        if bet_points is not None:
            s_player_balance = economy_utils.get_account_balance(second_user.id)
            if s_player_balance is None:
                self.__manage_rsp_state(lock_state=False)
                await init_msg.edit(
                    content="У второго игрока нет аккаунта с очками для ставок!"
                )
                await asyncio.sleep(self.fail_delay)
                await self.__purge_messages(messages_to_purge)
                return
            if s_player_balance < int(bet_points):
                self.__manage_rsp_state(lock_state=False)
                await init_msg.edit(
                    content="У второго игрока недостаточно очков для ставки!"
                )
                await asyncio.sleep(self.fail_delay)
                await self.__purge_messages(messages_to_purge)
                return
        await init_msg.edit(content="Сейчас идёт игра между "
                            f"{first_user.mention} и {second_user.mention}")
        try:
            await first_user.send("Ваш вариант *(На ответ 1 минута)*:")
            first_response = await self.client.wait_for(
                "message", timeout=30, check=self.__choice_check)
            users_choice.append(first_response.content.lower())
        except asyncio.TimeoutError:
            self.__manage_rsp_state(lock_state=False)
            f_move_fail = await current_channel.send(
                f"{first_user.mention} "
                "не успел ответить вовремя. "
                "Игра отменена")
            messages_to_purge.append(f_move_fail)
            await asyncio.sleep(self.fail_delay)
            await self.__purge_messages(messages_to_purge)
            return
        try:
            await second_user.send("Ваш вариант *(На ответ 1 минута)*:")
            second_response = await self.client.wait_for(
                "message", timeout=30, check=self.__choice_check)
            users_choice.append(second_response.content.lower())
        except asyncio.TimeoutError:
            self.__manage_rsp_state(lock_state=False)
            s_move_fail = await current_channel.send(
                f"{second_user.mention} "
                "не успел ответить вовремя. "
                "Игра отменена")
            messages_to_purge.append(s_move_fail)
            await asyncio.sleep(self.fail_delay)
            await self.__purge_messages(messages_to_purge)
            return
        self.__manage_rsp_state(lock_state=False)
        await current_channel.send(
            await self.__rsp_game(ctx, users_choice[0], users_choice[1], first_user.id,
                                  second_user.id, bet_points))
        await self.__purge_messages(messages_to_purge)

    @staticmethod
    def __manage_rsp_state(lock_state=False):
        """Lock or Unlock RSP game in database.

        This function locks/unlocks RSP game in database, so that only one game can be
        executed at a time.
        """
        database.modify_data("mainDB", "UPDATE variables SET rsp_game_active = ?",
                             1 if lock_state else 0)

    @staticmethod
    async def __purge_messages(messages):
        """Collect and delete all messages, that can distract users in channel.

        Args:
            message (list): List with messages to delete
        """
        for message in messages:
            await message.delete()

    @staticmethod
    def __join_check(ctx):
        """Check for correct conditions of join command.

        Args:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            bool: True if all conditions are met, False otherwise
        """
        test_string = ctx.content.lower()
        test_channel = isinstance(ctx.channel, discord.channel.DMChannel)
        return bool("играть" in test_string and not test_channel)

    @staticmethod
    def __choice_check(ctx):
        """Check for correct conditions of answer selection.

        Args:
            ctx (commands.context.Context): Context object to execute functions

        Returns:
            bool: True, if all conditions are met, False otherwise
        """
        test_string = ctx.content.lower()
        test_channel = isinstance(ctx.channel, discord.channel.DMChannel)
        return bool(test_string in WIN_VARIANTS and test_channel)


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(RSPGame(client))
