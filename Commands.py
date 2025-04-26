# test
import discord
import pymysql

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
async def before_command(ctx):

	await bot.wait_until_ready()
	if not DB_Manage.locate_member(ctx.author.id):
		DB_Manage.write_member(ctx.author.id, ctx.author, ctx.author.display_name)
#
# 	# if not isinstance(bot.userDB[context.author.id], context.command.permissions):
#     #     await context.send(f"Sorry, you don't have the valid permissions to run that command. This command can only be run by Bot {context.command.permissions.ranking}s and above.")


## Print Databases
@bot.command()
async def show_members(ctx):

	await ctx.send(DB_Manage.print_table("members"))
show_members.adminOnly = True

@bot.command()
async def shit_pants(ctx):

	raise Exception("NOOOOOOOOO")
shit_pants.adminOnly = False

@bot.command()
async def show_events(ctx):

	await ctx.send(DB_Manage.print_table("events"))
show_events.adminOnly = False

## Write Member to Database
@bot.command()
async def write_member(ctx, memberID, memberTag, memberName):

	DB_Manage.write_member(memberID, memberTag, memberName)
write_member.adminOnly = True

## Start Event Registration 
@bot.command()
async def start_registration(ctx, eventName, link):
	pass
start_registration.adminOnly = True

## Start Event
@bot.command()
async def start_event(ctx, eventName, startTimeStr = None):

	try:

		eventAttrs = DB_Manage.get_attrs("events", eventName)
		if eventAttrs["start"] is not None:

			await ctx.send("That event has already been started.")

			return

	except:

		pass

	if startTimeStr is None:

		startTime = time_now()

	else:

		startTime = Functions.str_to_secs(startTimeStr)

	bot.activeEvents[eventName] = await UI.event_card(ctx, bot, eventName, startTime)
start_event.adminOnly = True

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
start_meeting.adminOnly = True

## End Event Command
@bot.command()
async def end_event(ctx, eventName):

	if eventName not in bot.activeEvents.keys():

		await ctx.send("That event has not been started yet.")
		return

	eventAttrs = DB_Manage.get_attrs("events", eventName)

	if eventAttrs["isMeeting"] == 1:

		await ctx.send("Cannot end a meeting.")
		return

	startTime = eventAttrs["start"]
	if startTime is None:

		await ctx.send("Cannot end an event that has not started.")
		return



	# bot.activeEvents[eventName].embeds.send_data()
	#
	# DB_Manage.edit_attr("events", eventName, "end", endTime)
	# DB_Manage.edit_attr("events", eventName, "duration", endTime - startTime)
	#
	# await bot.activeEvents[eventName].delete()
	# del bot.activeEvents[eventName]
	#
	# await UI.send_message_card(ctx)

end_event.adminOnly = True

## Show Profile
@bot.command()
async def show_profile(ctx, memberTag):

	member = await commands.MemberConverter().convert(ctx, memberTag)

	# Call UI function to display profile
	# ui_func_DisplayProfile(memberID)
show_profile.adminOnly = False

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
edit_member.adminOnly = True

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
edit_event.adminOnly = True

## Delete Member
@bot.command()
async def delete_member(ctx, memberID):

	# memberID = await commands.MemberConverter().convert(ctx, memberTag)

	# Call MySQL function to delete member
	DB_Manage.remove_member(memberID)
delete_member.adminOnly = True

## Delete Event
@bot.command()
async def delete_event(ctx, eventName):

	# Call MySQL function to delete event
	DB_Manage.remove_event(eventName)
delete_event.adminOnly = True

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
show_leaderboard.adminOnly = False

## Christian's Code
@bot.command()
async def surveyverify(ctx):
    embed = discord.Embed(
        title="Welcome to the TNG Discord",
        description="Click the button below to provide information for all TNG Events.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=VerifyView())
surveyverify.adminOnly = False