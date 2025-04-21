import discord
import pymysql

from UI import VerifyView,RegisterView,AttendView
from Member import Member
from UI import VerifyView,RegisterView,AttendView

from Bot import BotClient
from time import time as time_now, strftime as format_time_str, localtime as to_time_struct, strptime as parse_time_str, mktime as to_secs
from datetime import datetime

from UI import VerifyView,RegisterView,AttendView

import DB_Manage
import Functions

bot = BotClient(command_prefix = "?", intents = discord.Intents.all())

@bot.command()
async def print_db(ctx):

    await ctx.send(DB_Manage.print_members())
    pass

@bot.command()
async def member_status(ctx, arg1):

    ctx.author.ID = arg1
    await ctx.send(DB_Manage.get_status(ctx.author.ID))
    pass

@bot.command()
async def write_member(ctx, arg1, arg2, arg3):

    # make it take just the id -> use discord.py to get tag and name
    ID = arg1
    tag = arg2
    name = arg3

    newMember = Member(ID, tag, name)
    DB_Manage.write_member(newMember)


##Edit User Data Command
@bot.command()
async def start_registration(ctx, eventName, link):

	print(DB_Manage.write_event(title = eventName, isMeeting = 0, start = None))

	try:
		attrs = DB_Manage.get_attrs("events", eventName)
	except Exception:
		return await ctx.send(f"Event `{eventName}` not found.")
	

	embed = discord.Embed(
        title=attrs["title"],
        color=discord.Color.blue()
    )
	embed.add_field(
        name="Instructions",
        value="Click **ATTEND** to register.",
        inline=False
    )
	embed.add_field(
        name="🍽️ Food Poll",
        value="[Click here](https://google.com)",
        inline=False
    )
	
	view = AttendView(event_name=attrs["title"])
	await ctx.send(embed=embed, view=view)

## Start Event
@bot.command()
async def start_event(ctx, eventName, startTimeStr = None):

	if startTimeStr is None:

		startTime = time_now()

	else:

		startTime = to_secs(parse_time_str(startTimeStr, bot.dateTimeFmt))
	
	print(DB_Manage.write_event(title = eventName, isMeeting = 0, start = startTime))

	embed = discord.Embed(
        title=eventName,
        color=discord.Color.blue()
    )
	embed.add_field(name="Event Time",value=startTime,inline=False)
	embed.add_field(name="Need Help?",value="DM The Organization Director",inline=False)
	view = RegisterView()
	await ctx.send(embed=embed, view=view)

##Start Event Command
@bot.command()
async def start_meeting(ctx, startTimeStr = None):

	meetingName = format_time_str("Member Meeting %m/%d/%Y", to_time_struct())

	if startTimeStr is None:
		startTime = time_now()
	else:
		startTime = to_secs(parse_time_str(startTimeStr, bot.dateTimeFmt))

	endTime = startTime + (60 * 60) # Standard 1-hour event
	duration = endTime - startTime

	DB_Manage.write_event(title = meetingName, isMeeting = 1, start = startTime, end = endTime, duration = duration)

	embed = discord.Embed(
        title=meetingName,
        color=discord.Color.blue()
    )
	embed.add_field(name="Meeting Time",value=startTime,inline=False)
	embed.add_field(name="Need Help?",value="DM The Organization Director",inline=False)
	view = RegisterView()
	await ctx.send(embed=embed, view=view)

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
		endTime = to_secs(parse_time_str(endTimeStr, bot.dateTimeFmt))

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

	try:

		DB_Manage.edit_attr("events", eventName, attrName, newData)

	except Exception as error:

		await ctx.send(error)

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
# async def eventEnd(context, arg1):

# 	eventType = arg1

# 	#*#* Utilize the UI function *endEvent" to conclude a current event
# 	#There SHOULD only be one event at a time so the function shouldn't need to take any arguments

# 	#endEvent()

# 	pass

##See Active Events
@bot.command()
async def events_active(context, *args):

    #*#* Utilize the function to display active events

    #showEvents()?

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
        title="Event Title",
        description="Meeting place and Time.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Food Poll", value="[Click here](https://google.com)", inline=False)
    view = RegisterView()
    await ctx.send(embed=embed, view=view)

@bot.command()
async def attend(ctx, *, event_name: str):
    try:
        attrs = DB_Manage.get_attrs("events", event_name)
    except Exception:
        return await ctx.send(f"Event `{event_name}` not found.")

    embed = discord.Embed(
        title=attrs["title"],
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Instructions",
        value="Click **ATTEND** to register.",
        inline=False
    )
    embed.add_field(
        name="🍽️ Food Poll",
        value="[Click here](https://google.com)",
        inline=False
    )

    view = AttendView(event_name=attrs["title"])
    await ctx.send(embed=embed, view=view)
