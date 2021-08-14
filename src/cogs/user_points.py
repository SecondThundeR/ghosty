import asyncio
import src.utils.economy_utils as economy_utils
from discord.ext import commands


class UserPoints(commands.Cog):
    def __init__(self, client):
        """Initialize variables for UserPoints.

        Args:
            client (discord.client.Client): Current client object
        """
        self.client = client
        self.delete_time = 3

    @commands.command(aliases=['очки'])
    async def points_hub(self, ctx, command=None):
        if command == 'создать':
            await self.__create_account(ctx, ctx.author.id)
        elif command == 'удалить':
            await self.__delete_account(ctx, ctx.author.id)
        elif command == 'баланс':
            await self.__send_account_details(ctx, ctx.author.id)
        elif command == 'перевод':
            await self.__transfer_points_to_user(ctx, ctx.author.id)
        else:
            pass

    async def __create_account(self, ctx, user_id):
        create_status = economy_utils.add_new_account(user_id)
        if create_status:
            await ctx.reply(
                'Успешно создан платежный аккаунт! '
                f'Ваш стартовый баланс равен **{economy_utils.DEFAULT_BALANCE}** очков',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        await ctx.reply(
            'У вас уже есть аккаунт в базе данных!',
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __delete_account(self, ctx, user_id):
        delete_status = economy_utils.delete_account(user_id)
        if delete_status:
            await ctx.reply(
                'Успешно удалён платежный аккаунт!',
                delete_after=self.delete_time
            )
            await asyncio.sleep(self.delete_time)
            await ctx.message.delete()
            return
        await ctx.reply(
            'У вас нет активного аккаунта в базе данных!',
            delete_after=self.delete_time
        )
        await asyncio.sleep(self.delete_time)
        await ctx.message.delete()

    async def __send_account_details(self, ctx, user_id):
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
        if reciever_status is False:
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
        economy_utils.transfer_points(
            sender_id, receiver_id, points_to_send
        )
        await ask_msg.edit(
            content=f'Успешно переведено **{points_to_send}** очков '
                    f'пользователю {receiver_member.mention}'
        )
        await asyncio.sleep(self.delete_time)
        await self.__purge_messages(messages_to_purge)

    async def __purge_messages(self, messages):
        """Collect and delete all messages, that can distract users in channel.

        Args:
            message (list): List with messages to delete
        """
        for message in messages:
            await message.delete()

    @staticmethod
    def __num_check(ctx):
        return ctx.content.isnumeric()

    @staticmethod
    def __user_check(ctx):
        if ctx.content.startswith('<@!'):
            return True
        return False


def setup(client):
    """Entry point for loading extension."""
    client.add_cog(UserPoints(client))
