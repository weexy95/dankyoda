import json
import sys
import os
import discord


from discord.ext import commands
from dotenv import load_dotenv
from db import *
from utils.startup import *


load_dotenv()

token = os.getenv("TOKEN")
intents = discord.Intents.all()
config = get_config()

bot = commands.Bot(
	command_prefix=config['bot_prefix'],
	intents=intents,
	case_insensitive=True,
	allowed_mentions=discord.AllowedMentions(everyone=False),
	owner_ids=config['owners'],
)
# bot.remove_command("help")


if __name__ == '__main__':
	load_events(bot)
	print('')
	load_commands(bot)

	if not os.path.isfile("config.json"):
		exit("'config.json' not found! Please add it and try again.")
	else:
		with open("config.json") as file:
			config = json.load(file)

	bot.run(token)


else:
	raise RuntimeError("Make sure you're running the main.py file")
