import random

import aiohttp
import discord
import requests
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from utils import economy, colors, startup


def get_meme():
	subreddits = ['memes', 'dankmemes']
	subreddit = random.choice(subreddits)
	url = f'https://meme-api.herokuapp.com/gimme/{subreddit}'
	response = requests.get(url)
	post = response.json()
	image = post['url']  # the meme (a reddit post)
	title = post['title']  # the title of the reddit post

	return [post, image, title]


def bool_str(variable):  # Function to convert boolean values to string: Yes/No
	if variable:
		return 'Yes'
	if not variable:
		return 'No'


class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = startup.get_config()

	@commands.command(name="8ball", aliases=["8b", "yesno"], usage="<question>", help="Get a random answer in yes/no by me for your question!")
	@commands.cooldown(1, 5, BucketType.user)
	async def eight_ball(self, context, *, question):
		answers = [
			'It is certain.',
			'It is decidedly so.',
			'You may rely on it.',
			'Without a doubt.',
			'Yes - definitely.',
			'As I see, yes.',
			'Most likely.',
			'Outlook good.',
			'Yes.',
			'Signs point to yes.',
			'Reply hazy, try again.',
			'Ask again later.',
			'Better not tell you now.',
			'Cannot predict now.',
			'Concentrate and ask again later.',
			'Don\'t count on it.', 'My reply is no.',
			'My sources say no.',
			'Outlook not so good.',
			'Very doubtful.',
			"nah",
			'...',
			'lol'
		]
		embed = discord.Embed(
			title=f"{question}",
			description=f"```{answers[random.randint(0, len(answers))]}```",
			color=0x42F56C
		)
		await context.send(embed=embed)

		@commands.command(name='cursed', aliases=['cursedimage'], help="Brings a post from r/cursed_images")
		@cooldown(1, 3, BucketType.user)
		async def cursed_image(self, ctx):
			url = f'https://meme-api.herokuapp.com/gimme/cursed_images'  # url of the api
			"""
            There is reddit's official API too, but it's slower and also sometimes returns mp4(s) that the discord.Embed class can't process. This API is much better in my opinion. Also, both, this and reddit's API are free.
            """

			response = requests.get(url)
			post = response.json()
			image = post['url']  # the meme (a reddit post)
			title = post['title']  # the title of the reddit post

			em = discord.Embed(
				title=title,
				color=discord.Color.random()
			)
			em.set_image(url=image)
			em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

			await ctx.send(embed=em)

	@commands.command(name='cursed', aliases=['cursedimage'], help="Brings a post from r/cursed_images and r/cursed")
	@cooldown(1, 3, BucketType.user)
	async def cursed_image(self, ctx):
		url = f'https://meme-api.herokuapp.com/gimme/{random.choice(["cursed", "cursedimages"])}'

		response = requests.get(url)
		post = response.json()
		image = post['url']  # the meme (a reddit post)
		title = post['title']  # the title of the reddit post

		em = discord.Embed(
			title=title,
			color=discord.Color.random()
		)
		em.set_image(url=image)
		em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

		await ctx.send(embed=em)

	@commands.command(name="fact", description="Get a useless fact, They're pretty good!")
	@commands.cooldown(1, 7, BucketType.user)
	async def fact(self, context):
		async with aiohttp.ClientSession() as session:
			async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
				if request.status == 200:
					data = await request.json()
					fact = data['text']
					embed = discord.Embed(description=fact, color=0xD75BF4)
					await context.send(embed=embed)
				else:
					return

	@commands.command(name='meme', aliases=['maymay', 'm'], help="Brings a post from meme subreddits..")
	@cooldown(1, 3, BucketType.user)
	async def meme(self, ctx):
		async def next_meme_callback(interaction):
			my_meme = get_meme()
			may = my_meme[0]
			memage = my_meme[1]
			mimle = my_meme[2]
			membed = interaction.message.embeds[0]
			membed.set_image(url=memage)
			membed.title = mimle
			membed.set_footer(text=f"👍 {may['ups']} | Author: u/{may['author']}")
			membed.color = discord.Color.random()

			await interaction.message.edit(embed=membed)

		async def close_meme_view(interaction):
			await interaction.message.edit(view=None)

		async def timeout_view():
			await message.edit(view=None)

		meme = get_meme()
		post = meme[0]
		image = meme[1]
		title = meme[2]
		meme_view = discord.ui.View(timeout=15)
		next_meme = discord.ui.Button(label="Next meme!", style=discord.ButtonStyle.green)
		next_meme.callback = next_meme_callback
		close_view = discord.ui.Button(emoji="<:x_white:930381127535984641>", style=discord.ButtonStyle.danger)
		close_view.callback = close_meme_view
		meme_view.add_item(next_meme)
		meme_view.add_item(close_view)
		meme_view.on_timeout = timeout_view

		em = discord.Embed(
			title=title,
			color=discord.Color.random())
		em.set_image(url=image)
		em.set_footer(text=f"👍 {post['ups']} | Author: u/{post['author']}")

		message = await ctx.send(embed=em, view=meme_view)

	@commands.command(name='roast', aliases=['insult'], help="Bully someone by roasting them, bad kid!", usage="[user]")
	@commands.cooldown(1, 5, BucketType.user)
	async def roast(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.author

		if user.bot:
			await ctx.send("I'm not gonna roast someone of my own kind!")
			return

		url = 'https://insult.mattbas.org/api/en/insult.json'
		# Visit https://insult.matlabs.org/api/ for documentation
		response = requests.get(url, params={'who': user.mention}).json()
		await ctx.send(user.mention + response['insult'])


def setup(bot):
	bot.add_cog(Owner(bot))
