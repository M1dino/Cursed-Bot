# * Importing the files needed for bot
import discord
from discord.ext import commands

# * external data
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='~')
client = discord.Client()

@bot.event
async def on_ready():
	print("Cursed is ready for action")	

for fileName in os.listdir('./extensions'):
	if fileName.endswith('.py'):
		bot.load_extension(f"extensions.{fileName[:-3]}")

# ? running the bot
load_dotenv()
bot.run(os.environ['TOKEN'])