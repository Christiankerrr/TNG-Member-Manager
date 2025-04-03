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
	## display all commands --- I
	## edit event - by event name
	## edit meeting (perform any logic necessary: start time, end time)
	## delete member/delete event - by event/member name

	## before invoke:
		## add unrecognized members to database - identify tag and recognize



## Tested-Working Commands

## Print Database
@bot.command()
async def print_db(ctx):

	await ctx.send(DB_Manage.print_members())
	pass


## Write Member to Database
@bot.command()
async def write_member(ctx, id, attr, name):

	# make it take just the id -> use discord.py to get tag and name (?)

	newMember = Member(id, attr, name)
	DB_Manage.write_member(newMember)


## Untested Commands

## Get Member Status
@bot.command()
async def member_status(ctx, tag):

	tag = ctx.author.ID
	await ctx.send(DB_Manage.get_status(tag))
	pass

## Start Event Registration 
@bot.command()
async def event_registration(ctx, eventName, eventDur):

	# create blank event, send to aaron

	# Call UI function to display event registration info
	ui_func_EventRegistrDisplay(eventName, eventDur)
	pass

## Start Event
@bot.command()
async def start_event(ctx, eventName):

	# 
	# Call UI function to end event registration function
	ui_func_EndRegistration()
	await ctx.send("Event registration has ended, thank you for your responses!")
	# Call UI function to start an event with the sign in/out buttons
	ui_func_StartEvent(eventName)
	await ctx.send(eventName + " Event has begun! Have a great time everyone!")
	pass

## Start Meeting
@bot.command()
async def start_meeting(ctx, *args):

	startTime = current.time
	# add to db

	# Call UI function to start an event with the sign in/out buttons, doesn't need special name
	ui_func_StartMeeting()
	await ctx.send("Welcome to the meeting everyone! Please sign in at your earliest convenience.")
	pass

## End Event Command
@bot.command()
async def end_event(ctx, *args):

	# Call UI function to conclude event
	ui_func_EndEvent()
	await ctx.send("The current event has concluded.")
	pass

## Show Profile
@bot.command()
async def show_profile(ctx, arg1):

	arg1 = await commands.MemberConverter().convert(ctx, arg1)

	# Call UI function to display profile
	ui_func_DisplayProfile(arg1.id)
	pass

## Show Leaderboard
@bot.command()
async def show_leaderboard(ctx, *args):

	# yeahhhh not sure about this one lol
	pass

## Manually Chnage Data
@bot.command()
async def edit_data(ctx, memberTag, attrName, newData):

	await commands.MemberConverter().convert(ctx, memberTag)
	# Call MySQL function to update the databse with given parameters
	if updateDatabase(memberTag.id, attrName, newData) == True:
		await ctx.send("Data successfully changed to " + newData)
	else:
		await ctx.send("Manual data change failed, please try again.")
	pass

## Display All Commands
@bot.command()
async def help(ctx):
	
	# find a way to itemize and display commands...?
	# I don't think i can call a command ti just display it. this seems common enough that I could youtube it though
	pass