import utils.environment as env
from discord.ext import commands


extensions = ['cogs.events', 'cogs.commands']
bot = commands.Bot(command_prefix='!',
                   description='Helsinki GameDev Club Discord Bot')

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

    bot.run(env.get_discord_token(), bot=True, reconnect=True)
