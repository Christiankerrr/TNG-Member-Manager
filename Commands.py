# test
import discord
import pymysql

from Member import Member
from discord.ext import commands
from Bot import BotClient
from time import time as time_now, strftime as format_time_str, localtime as to_time_struct, strptime as parse_time_str, mktime as to_secs
from datetime import datetime

# from UI import VerifyView, send_diet, send_shirt_size, finish_survey

import DB_Manage
import Functions
import UI

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
@bot.before_invoke
async def before_command(context):

	await bot.wait_until_ready()
	if not DB_Manage.locate_member(context.author.id):
		DB_Manage.write_member(context.author.id, context.author, context.author.display_name)
#
# 	# if not isinstance(bot.userDB[context.author.id], context.command.permissions):
#     #     await context.send(f"Sorry, you don't have the valid permissions to run that command. This command can only be run by Bot {context.command.permissions.ranking}s and above.")


## Print Databases
@bot.command()
async def show_members(ctx):

	await ctx.send(DB_Manage.print_table("members"))

@bot.command()
async def shit_pants(ctx):

	raise Exception("NOOOOOOOOO")

@bot.command()
async def show_events(ctx):

	await ctx.send(DB_Manage.print_table("events"))

## Write Member to Database
@bot.command()
async def write_member(ctx, memberID, memberTag, memberName):

	DB_Manage.write_member(memberID, memberTag, memberName)

## Untested Commands

## Start Event Registration 
@bot.command()
async def start_registration(ctx, eventName, link):


	# need to add functionality where register button collects id
	# and send to DB?
	
	# embed = discord.Embed(
    #     title="Registration For 'Add Variable for events here'",
    #     color=discord.Color.blue()
    # )
	# embed.add_field(name="**Meeting Area**", value="Blank", inline=False)
	# embed.add_field(name="**Need help?**", value="[Message Blank](https://google.com)", inline=False)

	# view = discord.ui.View()
	# sign_in = discord.ui.Button(label="Sign in", style=discord.ButtonStyle.link, url="https://google.com")
	# sign_out = discord.ui.Button(label="Sign Out", style=discord.ButtonStyle.link, url="https://google.com")

	# view.add_item(sign_in)
	# view.add_item(sign_out)

	# await ctx.send(embed=embed, view=view)
	pass

## Start Event
@bot.command()
async def start_event(ctx, eventName, startTimeStr = None):

	if startTimeStr is None:

		startTime = time_now()

	else:

		startTime = Functions.str_to_secs(startTimeStr)
	
	print(DB_Manage.write_event(title = eventName, isMeeting = 0, start = startTime))

	await UI.sign_in_out(ctx, eventName, Functions.secs_to_str(startTime))

## Start Meeting
@bot.command()
async def start_meeting(ctx, startTimeStr = None):

	meetingName = format_time_str("Member Meeting %m/%d/%Y", to_time_struct())

	if startTimeStr is None:
		startTime = time_now()
	else:
		startTime = Functions.str_to_secs(startTimeStr)

	endTime = startTime + (60 * 60) # Standard 1-hour event
	duration = endTime - startTime

	DB_Manage.write_event(title = meetingName, isMeeting = 1, start = startTime, end = endTime, duration = duration)

	# # Call UI function to start an event with the sign in/out buttons, doesn't need special name
	# ui_func_StartMeeting()
	await ctx.send("Welcome to the meeting everyone! Please sign in at your earliest convenience.")

## End Event Command
@bot.command()
async def end_event(ctx, eventName, endTimeStr = None):

	eventAttrs = DB_Manage.get_attrs("events", eventName)

	if eventAttrs["isMeeting"] == 1:

		await ctx.send("Can not end a meeting.")
		return

	startTime = eventAttrs["start"]
	if startTime is None:

		await ctx.send("Can not end an event that has not started.")
		return

	if endTimeStr is None:
		endTime = time_now()
	else:
		endTime = Functions.str_to_secs(endTimeStr)

	DB_Manage.edit_attr("events", eventName, "end", endTime)
	DB_Manage.edit_attr("events", eventName, "duration", endTime - startTime)
	# Call UI function to conclude event
	# ui_func_EndEvent()
	await ctx.send("The current event has concluded.")

## Show Profile
@bot.command()
async def show_profile(ctx, memberTag):

	member = await commands.MemberConverter().convert(ctx, memberTag)

	# Call UI function to display profile
	# ui_func_DisplayProfile(memberID)

## Manually Change Data
@bot.command()
async def edit_member(ctx, memberTag, attrName, newDataStr):

	member = await commands.MemberConverter().convert(ctx, memberTag)

	memberAttrs = DB_Manage.get_attrs("members", member.id)

	newData = Functions.sanitary_eval(newDataStr, locals = {"var": memberAttrs[attrName]})

	DB_Manage.edit_attr("members", member.id, attrName, newData)
	# Call MySQL function to update member databse with given parameters

	# if DB_Manage.edit_attr(memberTag.id, attrName, newData) == True:
	# 	await ctx.send("Data successfully changed to " + newData)
	# else:
	# 	await ctx.send("Manual data change failed, please try again.")

## Edit Event
@bot.command()
async def edit_event(ctx, eventName, attrName, newDataStr):

	eventAttrs = DB_Manage.get_attrs("events", eventName)

	newData = Functions.sanitary_eval(newDataStr, locals = {"var": eventAttrs[attrName]})

	if attrName in ("start", "end"):

		pass

	DB_Manage.edit_attr("events", eventName, attrName, newData)

	# 	if updateEvent(eventName, attrName, newData) == True:
	# 		await ctx.send("Event data successfully changed")
	# 	else:
	# 		await ctx.send("Data change failed, please try again.")

	# 	if updateEvent(eventName, attrName, newData) == True:
	# 		await ctx.send("Event data successfully changed")
	# 	else:
	# 		await ctx.send("Data change failed, please try again.")

## Delete Member
@bot.command()
async def delete_member(ctx, memberID):

	# memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call MySQL function to delete member
	DB_Manage.remove_member(memberID)

## Delete Event
@bot.command()
async def delete_event(ctx, eventName):

	# Call MySQL function to delete event
	DB_Manage.remove_event(eventName)


## Display All Commands
# @bot.command()
# async def help(ctx):
#
# 	# pre-existing help command? Involves cogs?
# 	pass


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