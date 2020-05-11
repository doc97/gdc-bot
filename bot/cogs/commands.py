from discord.ext import commands
import random


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coin', help='Flips a coin')
    async def _flip_coin(self, ctx):
        is_head = random.randint(1, 2) == 1
        msg = 'Heads!' if is_head else 'Tails!'
        await ctx.send(msg, tts=True)

    @commands.command(name='dice', help='Throws a d6')
    async def _roll_d6(self, ctx):
        num = random.choice(range(1, 7))
        await ctx.send(num, tts=True)


def setup(bot):
    bot.add_cog(Commands(bot))
