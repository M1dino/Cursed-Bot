import discord
from discord.ext import commands

import json
import random

from discord.ext.commands.core import command


# ? helper functions
def get_player_data():
	with open('./JSON/player_data.json', 'r') as data:
		obj = json.load(data)
	return obj

def set_player_data(data):
	with open('./JSON/player_data.json', 'w') as f:
		json.dump(data, f, indent = 4)

def random_element(userData):
	userData['player_data']['ingame_data']['element'] = random.choice(element_types)
	return userData


# * constants
# ? creating player JSON
CONST = {
	"player_data": {
		"user_data": {
			"user_id": 0,
			"character_name": '',
			"gender": "",
			"friends": [],
			"marriage": {},
			"verified": False
		},
		"ingame_data": {
			"class": None,
			"level": 0,
			"sub_class": {},
			"body_type": None,
			"element": None,
			"element_efficiency": "F",
			"special_element": {},
			"spirit": {},
			"inventory": [],
			"money": {
				"copper": 0,
				"silver": 0,
				"gold": 0
			},
			"equipment": {
				"weapon": {
					"right_hand": None,
					"left_hand": None,
				},
				"armour": {
					"left_arm": None,
					"right_arm": None,
					"body": None,
					"head": None,
					"legs": None,
					"feet": None
				}
			},
			"status": {
				"attack_power": 0,
				"defence_power": 0,
				"speed": 0,
				"health": 100,
				"fatigue": 0,
				"energy": 100,
				"luck": 0
			}
		}
	}
}

# ? adding body types
ECTO_STATUS = {
	"attack_power": 10,
	"defence_power": 5,
	"speed": 15,
	"health": 100,
	"fatigue": 0,
	"energy": 100,
	"luck": 10
}
MESO_STATUS = {
	"attack_power": 10,
	"defence_power": 10,
	"speed": 10,
	"health": 100,
	"fatigue": 0,
	"energy": 100,
	"luck": 10
}
ENDO_STATUS = {
	"attack_power": 10,
	"defence_power": 5,
	"speed": 15,
	"health": 100,
	"fatigue": 0,
	"energy": 100,
	"luck": 10
}

# ? elements
element_types = [
	'earth',
	'fire',
	'water',
	'wind',
	# 'air',
	'lightening'
]

# ? triple string texts
BODY_TYPE = '''
>>> Please select any one of these 3 body types

Ectomorph:
	__**Attack**__  - 10
	__**Defence**__ - 5
	__**Speed**__   - 15

Mesomorph:
	__**Attack**__  - 10
	__**Defence**__ - 10
	__**Speed**__   - 10

Endomorph:
	__**Attack**__  - 10
	__**Defence**__ - 15
	__**Speed**__   - 5
'''	

CLASS = '''
>>> Please select any one of the classes
Adventurer:
	Get to work with the Hunter's Association and carry out tasks for the better well being of the populus.
	*More information coming soon...*

Merchant:
	*More information coming soon...*

soldier:
	*More information coming soon...*
'''


class PlayerCreation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # * Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Player creator is online')
    
    # * Creating the character
    @commands.command(aliases=['c', 'Create', 'CREATE', 'GIMME'])
    async def create(self, context, *, username=''):
        if len(username) == 0:
            return await context.send(f"{'<@'+ str(context.author.id) + '>'} please enter a username")

        data = get_player_data() # * gettign the data in database

        # * testing for duplication
        if len(data) >= 1:
            for item in data:
                if item['player_data']['user_data']['user_id'] == context.author.id:
                    return await context.send('You can only have one character at a time')
                if item['player_data']['user_data']['character_name'].lower() == username.lower():
                    return await context.send('Character name is already taken, please choose another name')

        # * Adding user data
        data.append(CONST)
        data[len(data)-1]["player_data"]["user_data"]['user_id'] = context.author.id
        data[len(data)-1]["player_data"]["user_data"]['character_name'] = username
        await context.send('Please enter a valid gender of your character')

        # ? Checking for second msg
        def check(message):
            return message.author == context.author and message.channel == context.channel and message.content.lower() in (
                'male', 'guy', 'dude', 'boy', 'boi', 'bro', 'brother', 'female', 'gurl', 'girl', 'dudeette', 'sister', 'sis', 'thot'
            )
        message = await self.bot.wait_for('message', check=check)
        choice = message.content.lower()

        # ! testing the gender and appending the data
        if choice == 'male' or choice == 'guy' or choice == 'dude' or choice == 'boy' or choice == 'boi' or choice == 'bro' or choice == 'brother':
            data[len(data)-1]["player_data"]["user_data"]['gender'] = 'male'
            set_player_data(data)
            await context.send(f"Welcome {'<@'+str(context.author.id)+'>'} to the world of Spirits \n Please type ***~bodybuild*** or ***~bb*** to select your character's starter status")
        
        elif choice == 'female' or choice == 'gurl' or choice == 'girl' or choice == 'dudeette' or choice == 'sister' or choice == 'sis' or choice == 'thot':
            data[len(data)-1]["player_data"]["user_data"]['gender'] = 'female'
            set_player_data(data)
            await context.send(f"Welcome {'<@'+str(context.author.id)+'>'} to the world of Spirits \n Please type ***~bodybuild*** or ***~bb*** to select your character's starter status")

    # * Adding a body type
    @commands.command(aliases=['bb', 'BODYBUILD', 'BodyBuild'])
    async def bodybuild(self, context):
        data = get_player_data()
        isUserCreated = False
        index = 0

        # * testing if user exists
        if len(data) >= 1:
            for item in data:
                index += 1
                if context.author.id == item['player_data']['user_data']['user_id']:
                    await context.send(BODY_TYPE)
                    userData = item
                    isUserCreated = True
                    break
            if isUserCreated is False:
                return await context.send("Please create a character")
        else:
            return await context.send("Please create a character")
        
        # ? Checking for input
        def check(message):
            return message.author == context.author and message.channel == context.channel and message.content.lower() in (
                'ectomorph', 'mesomorph', 'endomorph'
            )
        message = await self.bot.wait_for('message', check=check)
        choice = message.content.lower()
        
        # ? making decision based on user input
        if choice == 'ectomorph':
            userData['player_data']['ingame_data']['body_type'] = 'Ectomorph'
            userData['player_data']['ingame_data']['status'] = ECTO_STATUS
            data[index-1] = userData
            set_player_data(data)
            if userData['player_data']['ingame_data']['class']:
                userData['player_data']['user_data']['verified'] = True
            return await context.send(f"{'<@'+str(context.author.id)+'>'} please type ***~class*** to select your class")

        elif choice == 'mesomorph':
            userData['player_data']['ingame_data']['body_type'] = 'Mesomorph'
            userData['player_data']['ingame_data']['status'] = MESO_STATUS
            data[index-1] = userData
            set_player_data(data)
            if userData['player_data']['ingame_data']['class']:
                userData['player_data']['user_data']['verified'] = True
            return await context.send(f"{'<@'+str(context.author.id)+'>'} please type ***~class*** to select your class")

        elif choice == 'endomorph':
            userData['player_data']['ingame_data']['body_type'] = 'Endomorph'
            userData['player_data']['ingame_data']['status'] = ENDO_STATUS
            data[index-1] = userData
            set_player_data(data)
            if userData['player_data']['ingame_data']['class']:
                userData['player_data']['user_data']['verified'] = True
            return await context.send(f"{'<@'+str(context.author.id)+'>'} please type ***~class*** to select your class")
    
    # * Adding class
    @commands.command(aliases=['class', 'Class', 'CLASS', 'cl', 'cls'])
    async def _class(self, context):
        data = get_player_data()
        isUserCreated = False
        index = 0

        # * testing if user is there
        if len(data) >= 1:
            for item in data:
                index += 1
                if context.author.id == item['player_data']['user_data']['user_id']:
                    await context.send(CLASS)
                    userData = item
                    isUserCreated = True
                    break
            if isUserCreated is False:
                return await context.send("Please create a character")
        else:
            return await context.send("Please create a character")
        
        # ? Checking for input
        def check(message):
            return message.author == context.author and message.channel == context.channel and message.content.lower() in (
                'adventurer', 'merchant', 'soldier'
            )
        message = await self.bot.wait_for('message', check=check)
        choice = message.content.lower()

        if choice == 'adventurer':
            userData['player_data']['ingame_data']['class'] = 'Adventurer'
            if userData['player_data']['ingame_data']['body_type']:
                userData['player_data']['user_data']['verified'] = True
            userData = random_element(userData)
            data[index-1] = userData
            set_player_data(data)
            return await context.send(f"Welcome {userData['player_data']['user_data']['character_name']} Adventurer! Please type ***~guild*** so that you could join a guild and be on your way to a new adventure")
        
        elif choice == 'merchant':
            userData['player_data']['ingame_data']['class'] = 'Merchant'
            if userData['player_data']['ingame_data']['body_type']:
                userData['player_data']['user_data']['verified'] = True
            userData = random_element(userData)
            data[index-1] = userData
            set_player_data(data)
            return await context.send(f"Welcome {userData['player_data']['user_data']['character_name']} fellow merchant! Please type ***~guild*** so that you could join a guild and be on your way to a new adventure")
        
        elif choice == 'soldier':
            userData['player_data']['ingame_data']['class'] = 'Soldier'
            if userData['player_data']['ingame_data']['body_type']:
                userData['player_data']['user_data']['verified'] = True
            userData = random_element(userData)
            data[index-1] = userData
            set_player_data(data)
            return await context.send(f"Welcome {userData['player_data']['user_data']['character_name']} Soldier! Please type ***~household*** so that you could get to work right away")



def setup(bot):
    bot.add_cog(PlayerCreation(bot))