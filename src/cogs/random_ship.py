"""Ship randomly selected users.

This cog allows user to ship two random people or two chosen by user.
Cog sends halves of each name and adds a heart.
"""


import emoji
import asyncio
import datetime as dt
import src.lib.database as database
import src.lib.users as users
import src.utils.shipping_utils as shipping_utils
from src.lib.exceptions import UsersNotFound
from discord.ext import commands


class RandomShip(commands.Cog):
    """Class to send message on behalf of a bot.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        ship_func_chooser: Selects correct ship mode
        get_user_info: Gets info about two selected users
        reset_ship: Reset all needed data in database
        custom_ship: Execute shipping with custom arguments
        random_ship: Execute shipping with random users
        random_ship_messages: Sends "prepare" message of random shipping
    """

    def __init__(self, client):
        """Initialize variables for RandomShip.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delay_time = 1
        self.delete_time = 5
        self.strings_to_send = [
            '*чтож...*', '**МОРЕ ВОЛНУЕТСЯ РАЗ**',
            '**МОРЕ ВОЛНУЕТСЯ ДВА**', '**МОРЕ ВОЛНУЕТСЯ ТРИ**'
        ]
        self.weekday_dict = {
            0: 'в Понедельник',
            1: 'во Вторник',
            2: 'в Среду',
            3: 'в Четверг',
            4: 'в Пятницу',
            5: 'в Субботу',
            6: 'в Воскресенье',
        }

    @commands.command(aliases=['шип'])
    async def ship_func_chooser(self, ctx, *args):
        """Select correct function depending of statement.

        This function chooses another function to run, when
        certain statement is true

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (tuple): List of arguments

        Returns:
            None: If there is an active shipping
        """
        if database.get_data(
            'mainDB',
            True,
            'SELECT ship_in_active FROM variables'
        ):
            return
        if len(args) == 1:
            if 'скип' in args:
                await RandomShip.reset_ship(self, ctx)
            elif 'фаст' in args:
                await RandomShip.random_ship(self, ctx, True)
            elif 'реролл' in args:
                await RandomShip.reset_ship(self, ctx, False)
                await RandomShip.random_ship(self, ctx)
            elif 'выйти' in args or 'войти' in args:
                await RandomShip.manage_ship_ignore(self, ctx, ctx.author.id, args[0])
            else:
                await ctx.reply('Я не могу шипперить одного человека. '
                                'Добавьте ещё кого-то, чтобы я смог '
                                'сделать "магию"')
        elif len(args) == 2:
            await RandomShip.custom_ship(self, ctx, list(args))
        else:
            await RandomShip.random_ship(self, ctx)

    async def manage_ship_ignore(self, ctx, user_id, mode):
        """Manage ignore list of shipping users.

        This function helps users to opt out of shipping or
        opt in.

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user_id (int): ID of user to ignore/add
            mode (str): Mode of operation with ignore list
        """
        user_state = database.get_data(
            'mainDB',
            True,
            'SELECT * FROM ignored_users WHERE users_id = ?',
            user_id
        )
        if mode == 'выход':
            if user_state is None:
                database.modify_data(
                    "mainDB",
                    "INSERT INTO ignored_users VALUES (?)",
                    user_id
                )
                database.modify_data(
                    "mainDB",
                    "DELETE FROM users WHERE users_id = ?",
                    user_id
                )
                await ctx.reply('Вы были убраны из списка участников шиппинга!',
                                delete_after=self.delete_time)
                await asyncio.sleep(self.delete_time)
                await ctx.message.delete()
                return
            await ctx.reply('Вы не учавствуете в шиппинге!',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if user_state is not None:
            database.modify_data(
                "mainDB",
                "DELETE FROM ignored_users WHERE users_id = ?",
                user_id
            )
            database.modify_data(
                "mainDB",
                "INSERT INTO users VALUES (?)",
                user_id
            )
            await ctx.reply("Вы были добавлены в список участников шиппинга!",
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        await ctx.reply("Вы уже учавствуете в шиппинге!",
                        delete_after=self.delete_time)
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def get_user_info(self, ctx, user):
        """Get names of users from arguments.

        This function gets username if user provided mention of someone,
        otherwise return argument without changes

        Args:
            ctx (commands.context.Context): Context object to execute functions
            user (str): Custom names for shipping

        Returns:
            list: List with username and it's length divided by two
        """
        if user.startswith('<@!'):
            user_id = user[3:len(user) - 1]
            custom_member = await ctx.guild.fetch_member(user_id)
            user_name = users.get_members_name(custom_member)
            user_length = int(len(user_name) / 2)
        else:
            user_name = user
            user_length = int(len(user_name) / 2)
        return [user_name, user_length]

    async def reset_ship(self, ctx, notif=True):
        """Reset latest ship results to start over.

        This function resets results of shipping to allow user execute
        new ship function

        Args:
            ctx (commands.context.Context): Context object to execute functions
            notif (bool): Controls sending message about resetting results
        """
        database.modify_data(
            'mainDB',
            'UPDATE variables SET ship_date = ?, ship_text_short = ?, '
            'ship_text_full = ?, ship_activated = ?',
            '',
            '',
            '',
            0
        )
        if notif:
            await ctx.reply('Результаты шиппинга сброшены! '
                            '*(Вы разлучили, возможно, великолепную парочку!)*',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()

    async def custom_ship(self, ctx, args):
        """Ship with two custom names from user.

        This function runs ship with two custom names from arguments,
        rather ship with random users

        Args:
            ctx (commands.context.Context): Context object to execute functions
            args (list): List of arguments (Custom names for ship)
        """
        if emoji.emoji_count(ctx.message.content):
            await ctx.reply('К сожалению, шип смайлов не имеет смысла',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '<@&' in args:
            await ctx.reply('К сожалению, я не могу обработать это',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '<:' in args:
            await ctx.reply('К сожалению, шип эмодзи не имеет смысла',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        elif '@everyone' in args or '@here' in args:
            await ctx.reply('Похоже вы пытаетесь передать `@here` или `@everyone`, '
                            'что может вызвать ошибку',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
        else:
            first_user_info = await RandomShip.get_user_info(self, ctx, args[0])
            second_user_info = await RandomShip.get_user_info(self, ctx, args[1])
            first_username_part = first_user_info[0][:first_user_info[1]]
            second_username_part = second_user_info[0][second_user_info[1]:]
            final_name = first_username_part + second_username_part
            await ctx.reply(f'Данная парочка смело бы называлась - **{final_name}**')

    async def random_ship(self, ctx, fast_mode=False):
        """Ship with two randomly chosen names.

        This function runs ship with random users,
        rather shipping two custom names from arguments

        Args:
            ctx (commands.context.Context): Context object to execute functions
            fast_mode (bool): Skip 'prelude' part before results

        Returns:
            None: If there is an error
        """
        try:
            users_info = await users.get_shipping_users(ctx.message)
        except UsersNotFound as warning:
            await ctx.reply(f'Произошла ошибка: {warning}!',
                            delete_after=self.delete_time)
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        current_date = dt.datetime.now().date()
        next_date = (dt.datetime.now() + dt.timedelta(days=1)).date()
        ship_data = shipping_utils.get_ship_data()
        if ship_data['ship_in_active']:
            return
        if not ship_data['ship_activated'] and not ship_data['ship_in_active']:
            await shipping_utils.lock_shipping()
            formatted_data = await shipping_utils.format_usernames(users_info)
            if fast_mode:
                await ctx.reply(f'**Парочка дня на сегодня:** {formatted_data[0]} '
                                ':two_hearts:')
            else:
                await RandomShip.random_ship_messages(self, ctx, formatted_data[0])
            database.modify_data(
                'mainDB',
                'UPDATE variables SET ship_date = ?, ship_text_full = ?, '
                'ship_text_short = ?, ship_in_active = ?',
                next_date,
                formatted_data[1],
                formatted_data[0],
                0
            )
        elif ship_data['ship_activated'] and current_date < dt.datetime.strptime(
            ship_data['ship_date'],
            '%Y-%m-%d'
        ).date():
            ship_text_full = database.get_data(
                'mainDB',
                True,
                'SELECT ship_text_full FROM variables'
            )
            next_date = database.get_data(
                'mainDB',
                True,
                'SELECT ship_date FROM variables'
            )
            next_date_string = self.weekday_dict[
                dt.datetime.strptime(next_date, '%Y-%m-%d').weekday()
            ]
            await ctx.reply(f'**Парочка дня на сегодня:** {ship_text_full} '
                            ':two_hearts: \n\n*Следующий шиппинг будет доступен '
                            f'{next_date_string}*')
        elif ship_data['ship_activated'] and current_date >= dt.datetime.strptime(
            ship_data['ship_date'],
            '%Y-%m-%d'
        ).date():
            database.modify_data(
                'mainDB',
                'UPDATE variables SET ship_activated = ?',
                0
            )
            await RandomShip.random_ship(self, ctx)

    async def random_ship_messages(self, ctx, short_text):
        """Send pre-messages and result of shipping.

        This function ships three pre-messages and final message with
        result of shipping

        Args:
            ctx (commands.context.Context): Context object to execute functions
            short_text (str): Ship's short text
        """
        for strings in self.strings_to_send:
            await ctx.channel.send(strings)
            await asyncio.sleep(self.delay_time)
        await ctx.send(f'**В ЛЮБОВНОЙ ПОЗЕ ЗАСТРЯЛИ** {short_text} :two_hearts:')


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(RandomShip(client))
