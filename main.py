# Importing the files needed for bot
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='~')

@bot.event
async def on_read():
  print("Cursed is read for action")