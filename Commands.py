import discord
import pymysql
import DB_Manage
from Member import Member

from Bot import BotClient

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
async def edit_data(ctx, arg1, arg2, arg3):

	memberTag = arg1
	attrName = arg2
	newData = arg3

	#*#* Need to utilize the get_connection() function to establish connection to MySQL

		# tngDB, cursor = get_connection()
		# updateDatabase(memberID, infoType, newData)
		# if updateDatabe = true:
		# 	await context.send(memberID + "'s" + infoType + " is now set to " + newData)
		# else:
		# 	await context.send("Manual data change failed, please try again.")

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

##Start Event Command
@bot.command()
async def eventStart(context, arg1): ##Separate need names of special events

	eventType = arg1

	#*#* Utilize the UI function *startEvent" to start an event with the sign in/out buttons

	# if eventType == "regular":
	# 	startEvent(eventType)
	# 	pass
	# elif eventType == "special":
	# 	startEvent(eventType)
	# 	pass
	# else:
	# 	await context.send("Unknown event type, please enter another command or try again")
	pass

# ##End Event Command
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