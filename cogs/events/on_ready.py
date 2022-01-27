import discord
import json

from discord.ext import commands
from pytz import timezone
from datetime import datetime
from utils.colors import *


class OnReady(commands.Cog):
	def __init__(self, client):
		self.client = client
		with open("config.json") as file:
			self.config = json.load(file)

	@commands.Cog.listener()
	async def on_ready(self):
		print('------------------')
		print(f"{t_blue}Time: {datetime.now(timezone('Asia/Kolkata')).strftime('%H:%M')} {datetime.now(timezone('Asia/Kolkata')).strftime('%d - %m - %Y')}")
		print(f"Servers: {(len(self.client.guilds))}")
		print(f"Users: {len(self.client.users)} {t_white}")
		print("-------------------")

		await self.client.change_presence(
			activity=discord.Activity(
				name=f"{self.config['bot_prefix']} help",
				type=discord.ActivityType.listening
			))


def setup(client):
	client.add_cog(onReady(client))
