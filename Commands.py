# test
import discord
import pymysql
import DB_Manage

from Member import Member
from discord.ext import commands
from Bot import BotClient
# from UI import VerifyView, send_diet, send_shirt_size, finish_survey


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
	## edit event - by event name --- U
	## edit meeting (perform any logic necessary: start time, end time) --- U
	## delete member --- U
	## delete event --- U

	## extra dm to admin to verify sign in?


## Before Invoke
# Meant to add anyone not currently in the DB to the DB
# Additionally check permissions??
@bot.check
async def before_command(context):

	await bot.wait_until_ready()
	if DB_Manage.locate_member(context.author.id) == False:
		DB_Manage.write_member(context.author.id, context.author)

	# if not isinstance(bot.userDB[context.author.id], context.command.permissions):
    #     await context.send(f"Sorry, you don't have the valid permissions to run that command. This command can only be run by Bot {context.command.permissions.ranking}s and above.")


## Tested-Working Commands

## Print Database
@bot.command()
async def print_db(ctx):

	await ctx.send(DB_Manage.print_members())

## Write Member to Database
@bot.command()
async def write_member(ctx, id, attr, name):

	newMember = Member(id, attr, name)
	DB_Manage.write_member(newMember)


## Untested Commands

## Get Member Status
@bot.command()
async def member_status(ctx, memberTag):

	memberID = ctx.author.ID
	await ctx.send(DB_Manage.get_status(memberID))

## Start Event Registration 
@bot.command()
async def event_registration(ctx):

	# need to add functionality where register button collects id
	# and send to DB?
	embed = discord.Embed(
        title="Registration For 'Add Variable for events here'",
        color=discord.Color.blue()
    )
	embed.add_field(name="**Meeting Area**", value="Blank", inline=False)
	embed.add_field(name="**Need help?**", value="[Message Blank](https://google.com)", inline=False)

	view = discord.ui.View()
	sign_in = discord.ui.Button(label="Sign in", style=discord.ButtonStyle.link, url="https://google.com")
	sign_out = discord.ui.Button(label="Sign Out", style=discord.ButtonStyle.link, url="https://google.com")

	view.add_item(sign_in)
	view.add_item(sign_out)

	await ctx.send(embed=embed, view=view)

## Start Event
@bot.command()
async def start_event(ctx, eventName, startTime, endTime):

	DB_Manage.write_event(eventName, startTime, endTime)

	# Call UI function to end event registration function
	ui_func_EndRegistration()
	await ctx.send("Event registration has ended, thank you for your responses!")
	# Call UI function to start an event with the sign in/out buttons
	ui_func_StartEvent(eventName)
	await ctx.send(eventName + " Event has begun! Have a great time everyone!")

## Start Meeting
@bot.command()
async def start_meeting(ctx, eventName, startTime, endTime):

	DB_Manage.write_event(eventName, startTime, endTime)

	# Call UI function to start an event with the sign in/out buttons, doesn't need special name
	ui_func_StartMeeting()
	await ctx.send("Welcome to the meeting everyone! Please sign in at your earliest convenience.")

## End Event Command
@bot.command()
async def end_event(ctx, *args):

	# Call UI function to conclude event
	ui_func_EndEvent()
	await ctx.send("The current event has concluded.")

## Show Profile
@bot.command()
async def show_profile(ctx, memberTag):

	memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call UI function to display profile
	ui_func_DisplayProfile(memberID)

## Manually Change Data
@bot.command()
async def edit_data(ctx, memberTag, attrName, newData, mode = "member", ):

	memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call MySQL function to update member databse with given parameters
	DB_Manage.edit_attr(mode, memberID, attrName, newData)

	# if DB_Manage.edit_attr(memberTag.id, attrName, newData) == True:
	# 	await ctx.send("Data successfully changed to " + newData)
	# else:
	# 	await ctx.send("Manual data change failed, please try again.")

## Edit Event
@bot.command()
async def edit_event(ctx, eventName, attrName, newData, mode = "event"):

	if eventName.lower() == "meeting":
		# Assumption that the only thing that could change in meeting is the time?
		endTime = 60 + newData

		# Call MySQL function to update event database
		DB_Manage.edit_attr(mode, eventName.lower(), attrName, newData)
		DB_Manage.edit_attr(eventName, endTimeAttributeName, endTime)	

	# 	if updateEvent(eventName, attrName, newData) == True:
	# 		await ctx.send("Event data successfully changed")
	# 	else:
	# 		await ctx.send("Data change failed, please try again.")
	else:
	 	# Call MySQL function to update event database
		DB_Manage.edit_attr(mode, eventName.lower(), attrName, newData)	

	# 	if updateEvent(eventName, attrName, newData) == True:
	# 		await ctx.send("Event data successfully changed")
	# 	else:
	# 		await ctx.send("Data change failed, please try again.")

## Delete Member
@bot.command()
async def delete_member(ctx, memberTag):

	memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call MySQL function to delete member
	DB_Manage.remove_member(memberID)

## Delete Event
@bot.command()
async def delete_event(ctx, eventName):

	# Call MySQL function to delete event
	DB_Manage.remove_event(eventName)


## Display All Commands
@bot.command()
async def help(ctx):
	
	# pre-existing help command? Involves cogs?
	pass


## Show Leaderboard
@bot.command()
async def show_leaderboard(ctx, *args):

	# yeahhhh not sure about this one lol
	pass


## Christian's Code
@bot.command()
async def surveyverify(ctx):
    embed = discord.Embed(
        title="Welcome to the TNG Discord",
        description="Click the button below to provide information for all TNG Events.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=VerifyView())