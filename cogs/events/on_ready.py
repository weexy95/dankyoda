import discord
import json
from db import *

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from asyncio import sleep


def get_prefix():
	with open('prefix.json', 'r') as f:
		cache = json.load(f)

	return cache['bot_prefix']


class onReady(commands.Cog):
	def __init__(self, client):
		self.client = client
		with open("config.json") as file:
			self.config = json.load(file)

	@commands.Cog.listener()
	async def on_ready(self):
		print('------------------')
		print("Time:", datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M'), datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y'))
		print(f"Servers: {(len(self.client.guilds))}")
		print(f"Users: {len(self.client.users)}")
		print("-------------------")

		await self.client.change_presence(
			activity=discord.Activity(
				name=f"{self.config['bot_prefix']} help",
				type=discord.ActivityType.listening
			))


def setup(client):
	client.add_cog(onReady(client))
