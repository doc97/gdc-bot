from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print(f'user:\t{self.bot.user}')
        print(f'id:\t{self.bot.user.id}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!', tts=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msg = message.content.lower()

        if 'thanks' in msg or 'thank you' in msg:
            await self._reply(message, "You're welcome!")

    async def _reply(self, message, reply):
        await message.channel.send(reply, tts=True)


def setup(bot):
    bot.add_cog(Events(bot))
