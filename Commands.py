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

	## before invoke:
		## add unrecognized members to database - identify tag and recognize



## Tested-Working Commands

## Print Database
@bot.command()
async def print_db(ctx):

	await ctx.send(DB_Manage.print_members())

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

## Start Event Registration 
@bot.command()
async def event_registration(ctx, eventName, eventDur):

	# create blank event, send to aaron

	# Call UI function to display event registration info
	ui_func_EventRegistrDisplay(eventName, eventDur)

## Start Event
@bot.command()
async def start_event(ctx, eventName):

	# Call UI function to end event registration function
	ui_func_EndRegistration()
	await ctx.send("Event registration has ended, thank you for your responses!")
	# Call UI function to start an event with the sign in/out buttons
	ui_func_StartEvent(eventName)
	await ctx.send(eventName + " Event has begun! Have a great time everyone!")

## Start Meeting
@bot.command()
async def start_meeting(ctx, *args):

	startTime = current.time
	# add to db

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
	ui_func_DisplayProfile(arg1.id)

## Manually Chnage Data
@bot.command()
async def edit_data(ctx, memberTag, attrName, newData):

	memberID = await commands.MemberConverter().convert(ctx, memberTag)
	# Call MySQL function to update member databse with given parameters
	if updateMember(memberTag.id, attrName, newData) == True:
		await ctx.send("Data successfully changed to " + newData)
	else:
		await ctx.send("Manual data change failed, please try again.")

## Edit Event
@bot.command()
async def edit_event(ctx, eventName, attrName, newData):

	if eventName == "Meeting":
		# Assumption that the only thing that could change in meeting is the time?
		# startTime = newData
		endTime = 60 + newData
		updateEvent(eventName, attrName, newData)
		updateEvent(eventName, endTimeAttributeName, endTime)	

		# Call MySQL function to update event database
		if updateEvent(eventName, attrName, newData) == True:
			await ctx.send("Event data successfully changed")
		else:
			await ctx.send("Data change failed, please try again.")
	else:
		# Call MySQL function to update event database
		if updateEvent(eventName, attrName, newData) == True:
			await ctx.send("Event data successfully changed")
		else:
			await ctx.send("Data change failed, please try again.")

## Delete Member
@bot.command()
async def delete_member(ctx, memberTag):

	memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call MySQL function to delete member
	remove_member(memberID)

## Delete Event
@bot.command()
async def delete_event(ctx, eventName):

	# Call MySQL function to delete event
	remove_event(eventName)


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


@bot.command()
async def register(ctx):

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