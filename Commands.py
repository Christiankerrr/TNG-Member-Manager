import discord

from Bot import BotClient

bot = BotClient(command_prefix = "?", intents = discord.Intents.all())

##Edit User Data Command
@bot.command()
async def editData(context, *args):
	if not args:  # If no arguments are provided
		await context.send("Please enter the data to alter.")
		return

	async def locateData(arg):
		arg = arg.split(":")[0].lower()
		if arg == "fast":
			await context.send("Fast Pong!")
		elif arg == "slow":
			await context.send("Slow Pong...")
		elif arg == "normal":
			await context.send("Regular Pong!")
		else:
			await context.send("Unknown Pong Type")

	async def changeData(arg):
		return
	
    # Send a response for each argument
	for arg in args:
		await locateData(arg)
	
	pass

##Start Event Command
@bot.command()
async def eventStart(context, *args):

	pass

##End Event Command
@bot.command()
async def eventEnd(context, *args):

	pass

##See Active Events
@bot.command()
async def eventActive(context, *args):

	pass