import discord
from discord.ext import commands

import json
import random

def get_data():
	with open('./JSON/data.json', 'r') as data:
		obj = json.load(data)
	return obj

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # * events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun extentions ready for action')

    # * commands
    @commands.command(aliases=['8ball', 'gotem', 'answerme', '8BALL', '8ballz'])
    async def _8ball(self, context, *, question):
        data = get_data()
        _8ball_answers = data['8ball']
        await context.send(f"{'<@' + str(context.author.id) + '>'} {random.choice(_8ball_answers)}")
    
    # ! command specific errors
    @_8ball.error
    async def _8ball_error(self, context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send(f"Oi {'<@'+str(context.author.id)+'>'}, where's the questions u ass crack")


def setup(bot):
    bot.add_cog(FunCommands(bot))