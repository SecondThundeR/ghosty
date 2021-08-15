"""Text version of Russian Roulette game.

This cog handles game logic of Russian Roulette.
"""


import random
import asyncio
import src.lib.database as database
import src.lib.words_base as words_base
import src.utils.economy_utils as economy_utils
from discord.ext import commands


class RussianRoulette(commands.Cog):
    """Class to execute text version of Russian Roulette game.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        russian_roulette_handler: Handles logic of Russian Roulette
        __get_random_word: Gets random word from database for different scenarios
        __add_new_word: Adds new word to Russian Roulette DB
        __delete_exist_word: Deletes existing word from Russian Roulette DB
    """

    def __init__(self, client):
        """Initialize variables for RussianRoulette.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.tables_aliases = {
            'вин': 'win',
            'луз': 'lose',
            'ноль': 'zero',
            'минус': 'minus'
        }
        self.points_multiplier = {
            1: 2,
            2: 2.5,
            3: 3,
            4: 3.5,
            5: 4,
        }
        self.delete_time = 5
        self.delay_time = 2

    @commands.command(aliases=['рулетка'])
    async def russian_roulette_handler(self, ctx, *args):
        """Handle game logic and start game.

        This function handles all Russian Roulette logic.
        Also, it has certain checks for any non-standard situation

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Bullet count number)
        """
        if not args:
            bullet_count = 1
            game_points = None
        else:
            if args[0] == 'добавить':
                self.__add_new_word(ctx, args)
                return
            if args[0] == 'удалить':
                self.__delete_exist_word(ctx, args)
                return
        if args[0].isnumeric():
            bullet_count = int(args[0])
        else:
            await ctx.reply('Похоже вы передали не число.'
                            '\nПопробуйте ещё раз, '
                            'но уже с правильными данными')
            return
        if bullet_count == 0:
            await ctx.reply(self.__get_random_word("zero"))
            return
        if bullet_count < 0:
            await ctx.reply(self.__get_random_word("minus"))
            return
        if bullet_count == 6:
            await ctx.reply('Поздравляю! Вы гуль!')
            return
        if bullet_count > 6:
            await ctx.reply('Может стоит напомнить, '
                            'что по правилам русской рулетки, '
                            'можно брать только до 6 патронов, не?')
            return
        try:
            game_points = int(args[1])
            sub_status = economy_utils.subtract_points(ctx.author.id, game_points)
            if not sub_status:
                await ctx.reply('Похоже у вас нет активного аккаунта '
                                'или недостаточно средств для игры со ставкой!',
                                delete_after=self.delete_time)
                await asyncio.sleep(self.delete_time)
                await ctx.message.delete()
                return
        except IndexError:
            game_points = None
        bullet_list = []
        for _ in range(bullet_count):
            charged_section = random.randint(1, 6)
            while charged_section in bullet_list:
                charged_section = random.randint(1, 6)
            bullet_list.append(charged_section)
        deadly_bullet = random.randint(1, 6)
        if deadly_bullet in bullet_list:
            result_msg = await ctx.reply('**БАХ**')
            await asyncio.sleep(self.delay_time)
            if game_points is not None:
                await result_msg.edit(
                    content=f'{self.__get_random_word("lose")}\n\n'
                            f'Вы проиграли **{game_points}** очков!\n'
                            'Ваш баланс составляет: '
                            f'**{economy_utils.get_account_balance(ctx.author.id)}** '
                            'очков'
                )
                return
            await result_msg.edit(
                content=self.__get_random_word("lose")
            )
            return
        result_msg = await ctx.reply('*тишина*')
        await asyncio.sleep(self.delay_time)
        if game_points is not None:
            won_points = game_points * self.points_multiplier[bullet_count]
            new_points = game_points + won_points
            economy_utils.add_points(ctx.author.id, new_points)
            await result_msg.edit(
                content=f'{self.__get_random_word("win")}\n\n'
                        f'Вы выйграли **{int(won_points)}** очков!\n'
                        'Ваш баланс составляет: '
                        f'**{economy_utils.get_account_balance(ctx.author.id)}** '
                        'очков'
            )
            return
        await result_msg.edit(
            content=self.__get_random_word("win")
        )
        return

    @staticmethod
    def __get_random_word(condition):
        """Get random word from database.

        This function handles getting random word from DB
        depending on condition of game

        Args:
            condition (str): Condition of game when executed

        Returns:
            str: Random chosen word depending on condition
        """
        words_list = database.get_data(
            'wordsDB',
            False,
            f'SELECT words FROM roulette_{condition}_words'
        )
        return random.choice(words_list)

    async def __add_new_word(self, ctx, args):
        """Add new word to Russian Roulette DB.

        This function controls adding new word to DB,
        as well as simplifiying main code base.

        Also, there are checks for any non-standard situation,
        like if arguments tuple having less than 2 elements or
        user wrote wrong table alias.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Bullet count number)
        """
        if len(args) == 1:
            await ctx.reply(
                'Вы не передали никаких дополнительных аргументов!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if args[1] not in self.tables_aliases:
            await ctx.reply(
                'Вы указали неверное название таблицы. '
                'Доступные названия: '
                f'{", ".join(key for key in self.tables_aliases)}',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        table_to_modify = self.tables_aliases[args[1]]
        word_to_add = " ".join(args[2:])
        await ctx.reply(
            words_base.manage_r_words_tables(
                word_to_add,
                table_to_modify,
                delete_mode=False
            ),
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()
        return

    async def __delete_exist_word(self, ctx, args):
        """Delete existing word from Russian Roulette DB.

        This function controls deleting word from DB,
        as well as simplifiying main code base.

        Also, there are checks for any non-standard situation,
        like if arguments tuple having less than 2 elements,
        user wrote wrong table alias or user isn't bot admin.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Bullet count number)
        """
        if len(args) == 1:
            await ctx.reply(
                'Вы не передали никаких дополнительных аргументов!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if args[1] not in self.tables_aliases:
            await ctx.reply(
                'Вы указали неверное название таблицы. '
                'Доступные названия: '
                f'{", ".join(key for key in self.tables_aliases)}',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        bot_admin = database.get_data(
            'mainDB',
            True,
            'SELECT * FROM admin_list '
            'WHERE admins_id = ?',
            ctx.author.id
         )
        if bot_admin is None:
            await ctx.reply(
                'Вы не имеете необходимых прав для удаления слов. '
                'Удаление слов доступно администраторам бота',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        table_to_modify = self.tables_aliases[args[1]]
        word_to_delete = " ".join(args[2:])
        await ctx.reply(
            words_base.manage_r_words_tables(
                word_to_delete,
                table_to_modify,
                delete_mode=True
            ),
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()
        return


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(RussianRoulette(client))
