import discord

from discord.ext import commands
from db import *
import json


class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

        if not os.path.isfile("config.json"):
            exit("'config.json' not found! Please add it and try again.")

        with open("config.json", "r") as file:
            self.config = json.load(file)

        self.prefix = self.config['bot_prefix']


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if guild.me.guild_permissions.send_messages and guild.me.guild_permissions.embed_links:
                em = discord.Embed(
                    title='Hey there!',
                    description=f'Thanks for inviting me to your server.\nMy prefix is \'`{self.prefix}`\'',
                    color=0x60FF60
                )
                await channel.send(embed=em)
                break

        print(f"Joined new server, Name: {str(guild)}, ID: {guild.id}, Members: {len(guild.member_count)}")


def setup(client):
    client.add_cog(OnGuildJoin(client))
