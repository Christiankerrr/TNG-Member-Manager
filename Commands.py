import discord

from Bot import BotClient

bot = BotClient(command_prefix = "?", intents = discord.Intents.all())

@bot.command()
async def ping(context, *args):

	pass