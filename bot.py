import discord
from cogs.cogs import MainCogs
from cogs.musiccog import Music
from cogs.productivity import Productivity
from discord.ext import commands
import os
TOKEN = os.environ["TOKEN"]
activity = discord.Activity(type=discord.ActivityType.listening, name=">help")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', help_command=None, intents=intents, activity=activity, status=discord.Status.online)

@bot.event
async def on_ready():
    bot.add_cog(Productivity(bot))
    bot.add_cog(Music(bot))
    bot.add_cog(MainCogs(bot))
    print('{:^43}'.format('Logged in as'))
    print("{:^20} | {:^20}".format("Username", "User ID"))
    print("{:^20} | {:^20}".format(bot.user.name, bot.user.id))

bot.run(TOKEN)

