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
        __parse_args: Parses arguments and returns dictionary with data
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
        }
        self.backup_words = {
            'win': 'Вы победили!',
            'lose': 'Вы проиграли!',
            'zero': 'Нельзя играть с 0 пулями!'
        }
        self.points_multiplier = {
            1: 1.25,
            2: 1.5,
            3: 2,
            4: 2.5,
            5: 3,
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
        parsed_args = await self.__parse_args(ctx, args)
        if parsed_args is None or parsed_args["game_status"] == 1:
            return
        if parsed_args["bullet_count"] == 0:
            await ctx.reply(self.__get_random_word("zero"))
            return
        if parsed_args["bullet_count"] == 6:
            await ctx.reply('Поздравляю! Вы гуль!')
            return
        if parsed_args["bullet_count"] > 6:
            await ctx.reply('Может стоит напомнить, '
                            'что по правилам русской рулетки, '
                            'можно брать только до 6 патронов, не?')
            return
        if parsed_args["game_points"] is not None:
            self.__change_game_status(ctx, 1)
        bullet_list = []
        for _ in range(parsed_args["bullet_count"]):
            charged_section = random.randint(1, 6)
            while charged_section in bullet_list:
                charged_section = random.randint(1, 6)
            bullet_list.append(charged_section)
        deadly_bullet = random.randint(1, 6)
        if deadly_bullet in bullet_list:
            economy_utils.subtract_points(
                ctx.author.id, parsed_args["game_points"]
            )
            result_msg = await ctx.reply('**БАХ**')
            await asyncio.sleep(self.delay_time)
            if parsed_args["game_points"] is not None:
                await result_msg.edit(
                    content=f'{self.__get_random_word("lose")}\n\n'
                            f'Вы проиграли **{parsed_args["game_points"]}** очков!'
                )
                self.__change_game_status(ctx, 0)
                return
            await result_msg.edit(
                content=self.__get_random_word("lose")
            )
            return
        result_msg = await ctx.reply('*тишина*')
        await asyncio.sleep(self.delay_time)
        if parsed_args["game_points"] is not None:
            won_points = parsed_args["game_points"] * self.points_multiplier[
                parsed_args["bullet_count"]
            ]
            economy_utils.add_points(ctx.author.id, won_points)
            await result_msg.edit(
                content=f'{self.__get_random_word("win")}\n\n'
                        f'Вы выйграли **{won_points}** очков!'
            )
            self.__change_game_status(ctx, 0)
            return
        await result_msg.edit(
            content=self.__get_random_word("win")
        )
        return

    def __change_game_status(self, ctx, game_status):
        database.modify_data(
            'pointsDB',
            'UPDATE points_accounts SET active_roulette = ? WHERE user_id = ?',
            game_status, ctx.author.id
        )

    async def __parse_args(self, ctx, args):
        """Parse arguments and return dictionary with data.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments (Bullet count number and/or points)

        Returns:
            dict: Dictionary with parsed arguments
            None: If arguments are not valid
        """
        if not args:
            return {
                "bullet_count": 1,
                "game_points": None,
                "game_status": None
            }
        if len(args) == 1:
            if args[0] == 'добавить':
                self.__add_new_word(ctx, args)
                return
            if args[0] == 'удалить':
                self.__delete_exist_word(ctx, args)
                return
            if args[0].isnumeric():
                return {
                    "bullet_count": int(args[0]),
                    "game_points": None,
                    "game_status": None
                }
            await ctx.reply('Похоже вы передали неправильный аргумент.'
                            '\nПопробуйте ещё раз, '
                            'но уже с правильными данными')
            return
        if len(args) == 2:
            bullet_count = 1
            game_points = None
            game_status = None
            if args[0].isnumeric():
                bullet_count = int(args[0])
            if args[1].isnumeric():
                game_points = int(args[1])
            if game_points is not None:
                acc_balance = economy_utils.get_account_balance(ctx.author.id)
                if acc_balance is None:
                    await ctx.reply('Похоже у вас нет активного аккаунта '
                                    'для игры со ставкой!',
                                    delete_after=self.delete_time)
                    await asyncio.sleep(self.delete_time)
                    await ctx.message.delete()
                    return
                if acc_balance < game_points:
                    await ctx.reply('Похоже у вас недостаточно средств '
                                    'для игры со ставкой!',
                                    delete_after=self.delete_time)
                    await asyncio.sleep(self.delete_time)
                    await ctx.message.delete()
                    return
                game_status = database.get_data(
                    'pointsDB',
                    True,
                    "SELECT active_roulette FROM points_accounts "
                    "WHERE user_id = ?",
                    ctx.author.id
                )
            return {
                "bullet_count": bullet_count,
                "game_points": game_points,
                "game_status": game_status
            }

    def __get_random_word(self, condition):
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
        if words_list is None:
            return self.backup_words[condition]
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
