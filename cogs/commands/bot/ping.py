import json

import aiohttp
import discord
from discord.ui import *

from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, Cog


class Ping(Cog):
	def __init__(self, client):
		self.client = client
		with open("config.json") as file:
			self.config = json.load(file)

	@commands.command(
		name="ping",
		aliases=["latency"],
		help="Get stats on bot's running status and more!")
	# @commands.is_owner()
	async def ping(self, context):
		"""
		Check if the bot is running.
		"""
		embed = discord.Embed(
			description="🏓 Pong, The bot is running smooth and sharp!",
			color=0x42F56C
		)
		custom_view = View()
		custom_url = self.config['report_error_url']
		custom_label = 'Report an Issue!'
		custom_button = Button(label=custom_label, url=custom_url)
		custom_view.add_item(custom_button)

		await context.send(embed=embed, view=custom_view)


def setup(client):
	client.add_cog(Ping(client))
