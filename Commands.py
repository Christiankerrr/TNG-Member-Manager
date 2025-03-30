import discord
import pymysql
import DB_Manage

from Member import Member
from discord.ext import commands
from Bot import BotClient

bot = BotClient(command_prefix = "?", intents = discord.Intents.all())

## Command Key: -> C = Complete, U = Untested, I = Incomplete
	## print database --- C
	## write member to db --- C
	## get member status --- U
	## start event registration --- U
	## start event (auto end registration) --- U
	## start meeting --- U
	## end event/meeting --- U
	## show profile --- U
	## show leaderboard --- I
	## manually edit data --- U


## Tested-Working Commands

## Print Database
@bot.command()
async def print_db(ctx):

	await ctx.send(DB_Manage.print_members())
	pass


## Write Member to Database
@bot.command()
async def write_member(ctx, arg1, arg2, arg3):

	# make it take just the id -> use discord.py to get tag and name (?)
	ID = arg1
	attr = arg2
	name = arg3

	newMember = Member(ID, attr, name)
	DB_Manage.write_member(newMember)


## Untested Commands

## Get Member Status
@bot.command()
async def member_status(ctx, arg1):

	ctx.author.ID = arg1
	await ctx.send(DB_Manage.get_status(ctx.author.ID))
	pass

## Start Event Registration 
@bot.command()
async def event_registration(ctx, arg1, arg2):

	eventName = arg1
	eventDur = arg2

	# Call UI function to display event registration info
	ui_func_EventRegistrDisplay(eventName, eventDur)
	pass

## Start Event
@bot.command()
async def startEvent(ctx, arg1):

	eventName = arg1

	# Call UI function to end event registration function
	ui_func_EndRegistration()
	await ctx.send("Event registration has ended, thank you for your responses!")
	# Call UI function to start an event with the sign in/out buttons
	ui_func_StartEvent(eventName)
	await ctx.send(arg1 + " Event has begun! Have a great time everyone!")
	pass

## Start Meeting
@bot.command()
async def startMeeting(ctx, *args):

	# Call UI function to start an event with the sign in/out buttons, doesn't need special name
	ui_func_StartMeeting()
	await ctx.send("Welcome to the meeting everyone! Please sign in at your earliest convenience.")
	pass

## End Event Command
@bot.command()
async def endEvent(ctx, *args):

	# Call UI function to conclude event
	ui_func_EndEvent()
	await ctx.send("The current event has concluded.")
	pass

## Show Profile
@bot.command()
async def showProfile(ctx, arg1):

	arg1 = await commands.MemberConverter().convert(ctx, arg1)

	# Call UI function to display profile
	ui_func_DisplayProfile(arg1.id)
	pass

## Show Leaderboard
@bot.command()
async def showLeaderboard(ctx, *args):

	# yeahhhh not sure about this one lol
	pass

## Manually Chnage Data
@bot.command()
async def edit_data(ctx, arg1, arg2, arg3):

	memberTag = arg1
	attrName = arg2
	newData = arg3

	await commands.MemberConverter().convert(ctx, memberTag)
	# Call MySQL function to update the databse with given parameters
	if updateDatabase(memberTag.id, attrName, newData) == True:
		await ctx.send("Data successfully changed to " + newData)
	else:
		await ctx.send("Manual data change failed, please try again.")
	pass

##Multi-argument Ping-Pong example w/ ChatGPT [Don't need, just to help visualize multiple arguments]
# @bot.command()
# async def ping(ctx, *args):
#     if not args:  # If no arguments are provided
#         await ctx.send("❗ Please provide at least one argument (fast, slow, normal).")
#         return

#     async def send_pong(arg):
#         arg = arg.lower()
#         if arg == "fast":
#             await ctx.send("⚡ Fast Pong!")
#         elif arg == "slow":
#             await ctx.send("🐢 Slow Pong...")
#         elif arg == "normal":
#             await ctx.send("🏓 Regular Pong!")
#         else:
#             await ctx.send("❓ Unknown Pong Type")

#     # Send a response for each argument
#     for arg in args:
#         await send_pong(arg)