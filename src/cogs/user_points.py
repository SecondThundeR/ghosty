"""Manage points accounts in a user-friendly way.

This cog helps to manage points accounts
(adding/removing account, checking balance, etc)
in a user-friendly way.
"""

import asyncio
import src.utils.economy_utils as economy_utils
from discord.ext import commands


class UserPoints(commands.Cog):
    """Class to manage points accounts.

    Args:
        commands.Cog: Base class that all cogs must inherit from

    Methods:
        points_hub: Redirects to certain functions
        __create_account: Creates account for user
        __delete_account: Removes account for user
        __send_account_details: Returns account balance
        __transfer_points_to_user: Transfer points to user
        __daily_bonus_points: Manages giving daily bonus points
        __purge_messages: Purges service messages to clear channel
        __num_check: Check if user input is number
        __user_check: Check if message contains user ID
    """

    def __init__(self, client):
        """Initialize variables for UserPoints.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delete_time = 3

    @commands.command(aliases=['очки'])
    async def points_hub(self, ctx, arg=None):
        """Redirect to certain function based on command argument.

        Args:
            ctx (discord.ext.commands.Context): Context object
            arg (Union[str | None]): Command argument
        """
        if arg == 'создать':
            await self.__create_account(ctx, ctx.author.id)
        elif arg == 'удалить':
            await self.__delete_account(ctx, ctx.author.id)
        elif arg == 'баланс':
            await self.__send_account_details(ctx, ctx.author.id)
        elif arg == 'перевод':
            await self.__transfer_points_to_user(ctx, ctx.author.id)
        elif arg == 'бонус':
            await self.__daily_bonus_points(ctx, ctx.author.id)
        else:
            return

    async def __create_account(self, ctx, user_id):
        """Create points account for user.

        This function checks if user already has account, if not,
        creates new account and returns account start balance.

        Args:
            ctx (discord.ext.commands.Context): Context object
            user_id (str): ID of user
        """
        create_status = economy_utils.add_new_account(user_id)
        if create_status is False:
            await ctx.reply(
                'У вас уже есть аккаунт в базе данных!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if create_status is None:
            await ctx.reply(
                'Успешно создан платежный аккаунт! '
                f'Ваш стартовый баланс равен **{economy_utils.DEFAULT_BALANCE}** очков',
                delete_after=self.delete_time
            )
        elif create_status is True:
            await ctx.reply(
                'Успешно восстановлен платежный аккаунт! '
                f'Ваш баланс был сброшен до **{economy_utils.ZERO_BALANCE}** очков',
                delete_after=self.delete_time
            )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __delete_account(self, ctx, user_id):
        """Remove points account of user.

        This function checks if user has account, if yes,
        removes account, otherwise warn that account isn't created.

        Args:
            ctx (discord.ext.commands.Context): Context object
            user_id (str): ID of user
        """
        delete_status = economy_utils.delete_account(user_id)
        if delete_status:
            messages_to_purge = []
            ask_msg = await ctx.reply(
                "Вы уверены что хотите удалить свой аккаунт с очками? "
                "(Учтите, что при следующем создании, ваш баланс будет равен нулю)\n"
                "Чтобы продолжить, напишите **'Да'**",
            )
            messages_to_purge.append(ctx.message)
            messages_to_purge.append(ask_msg)
            try:
                answer_msg = await self.client.wait_for(
                    'message',
                    timeout=60,
                    check=self.__delete_check
                )
            except asyncio.TimeoutError:
                await ask_msg.edit(
                    content='Вы достигли таймаута! '
                    'Отменяю удаление акканута'
                )
                await asyncio.sleep(self.delete_time)
                await self.__purge_messages(messages_to_purge)
                return
            await answer_msg.delete()
            await ask_msg.edit(
                content='Я успешно удалил ваш аккаунт с очками!'
            )
            await asyncio.sleep(self.delete_time)
            await self.__purge_messages(messages_to_purge)
            return
        await ctx.reply(
            'У вас нет активного аккаунта в базе данных!',
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __send_account_details(self, ctx, user_id):
        """Return points account details.

        This function checks for user account, if exists,
        returns account balance.

        Args:
            ctx (discord.ext.commands.Context): Context object
            user_id (str): ID of user
        """
        account_balance = economy_utils.get_account_balance(user_id)
        if account_balance is None:
            await ctx.reply(
                'У вас нет активного аккаунта в базе данных!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        await ctx.reply(
            f'Ваш баланс равен: **{account_balance}** очков',
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __transfer_points_to_user(self, ctx, sender_id):
        """Transfer points from sender to reciever.

        This function helps to transfer points from sender to reciever.
        By using help questions and waiting for user input, it can
        get reciever ID and amount of points to transfer.

        Also it handles some errors and exceptions and warns about them.

        Args:
            ctx (discord.ext.commands.Context): Context object
            sender_id (str): ID of sender
        """
        sender_balance = economy_utils.get_account_balance(sender_id)
        if sender_balance is None:
            await ctx.reply(
                'У вас нет активного аккаунта в базе данных!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if sender_balance <= 0:
            await ctx.reply(
                'У вас недостаточно денег для перевода! '
                f'Ваш баланс равен: {sender_balance}',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        messages_to_purge = []
        ask_msg = await ctx.reply("Кому вы хотите перевести очки?")
        messages_to_purge.append(ctx.message)
        messages_to_purge.append(ask_msg)
        try:
            answer_msg = await self.client.wait_for(
                'message',
                timeout=60,
                check=self.__user_check
            )
        except asyncio.TimeoutError:
            await ask_msg.edit(
                content='Вы достигли таймаута! '
                'Отменяю активный перевод'
            )
            await asyncio.sleep(self.delete_time)
            await self.__purge_messages(messages_to_purge)
            return
        receiver_id = answer_msg.content[3:len(answer_msg.content) - 1]
        await answer_msg.delete()
        receiver_member = await ctx.message.guild.fetch_member(receiver_id)
        reciever_status = economy_utils.check_account(receiver_id)
        if not reciever_status:
            await ask_msg.edit(
                content=f'{receiver_member.mention} не имеет аккаунта в базе данных!'
            )
            await asyncio.sleep(self.delete_time)
            await self.__purge_messages(messages_to_purge)
            return
        await ask_msg.edit(
            content=f'Сколько вы хотите перевести очков для {receiver_member.mention}?'
        )
        try:
            answer_msg = await self.client.wait_for(
                'message',
                timeout=60,
                check=self.__num_check
            )
        except asyncio.TimeoutError:
            await ask_msg.edit(
                content='Вы достигли таймаута! '
                'Отменяю активный перевод'
            )
            await asyncio.sleep(self.delete_time)
            await self.__purge_messages(messages_to_purge)
            return
        points_to_send = int(answer_msg.content)
        await answer_msg.delete()
        transfer_status = economy_utils.transfer_points(
            sender_id, receiver_id, points_to_send
        )
        if not transfer_status:
            await ask_msg.edit(
                content=f'Перевод не удался! К сожелению, на аккаунте отправителя '
                        'недостаточно очков для перевода'
                        f'пользователю {receiver_member.mention}'
            )
            await asyncio.sleep(self.delete_time)
            await self.__purge_messages(messages_to_purge)
            return
        await ask_msg.edit(
            content=f'Успешно переведено **{points_to_send}** очков '
                    f'пользователю {receiver_member.mention}'
        )
        await asyncio.sleep(self.delete_time)
        await self.__purge_messages(messages_to_purge)

    async def __daily_bonus_points(self, ctx, user_id):
        """Manage getting daily bonus points.

        Args:
            ctx (discord.ext.commands.Context): Context object
            user_id (str): ID of user
        """
        daily_bonus_points = economy_utils.daily_points_manager(user_id)
        if daily_bonus_points is False:
            await ctx.reply(
                'У вас нет активного аккаунта с очками!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        if daily_bonus_points is None:
            await ctx.reply(
                'Похоже вы уже получали бонусные очки за сегодня!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        await ctx.reply(
            f'Поздравляем! Вы получили **{daily_bonus_points} очков**!\n'
            'Ваш баланс теперь равен '
            f'**{economy_utils.get_account_balance(user_id)} очков**',
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __purge_messages(self, messages):
        """Collect and delete all messages, that can distract users in channel.

        Args:
            message (list): List with messages to delete
        """
        for message in messages:
            await message.delete()

    @staticmethod
    def __num_check(ctx):
        """Check, if message is a number."""
        return ctx.content.isnumeric()

    @staticmethod
    def __user_check(ctx):
        """Check, if message contains user ID."""
        return bool(ctx.content.startswith('<@!'))

    @staticmethod
    def __delete_check(ctx):
        """Check, if user confirmed the deletion of the account"""
        return ctx.content.lower() == 'да'


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(UserPoints(client))
