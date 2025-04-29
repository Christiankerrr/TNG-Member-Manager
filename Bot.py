from discord.ext import commands, tasks
from time import time as time_now

from discord.ext.commands import Context, errors
from discord.ext.commands._types import BotT

import DB_Manage
import Functions

class BotClient(commands.Bot):

	@tasks.loop(hours = 24)
	async def update_member_db(self):

		tngServer = self.get_guild(self.tngServerID)

		totalEventHours = DB_Manage.get_total_hours()
		totalMeetings = DB_Manage.get_total_meetings()

		for discordID in DB_Manage.get_all_ids():

			memberAttrs = DB_Manage.get_attrs("members", discordID)

			memberObj = tngServer.fetch_member(discordID)
			DB_Manage.edit_attr("members", discordID, "tag", memberObj.name)
			DB_Manage.edit_attr("members", discordID, "name", memberObj.display_name)

			if Functions.is_exec(memberObj):

				if memberAttrs["hours"] < totalEventHours:

					DB_Manage.edit_attr("members", discordID, "hours", totalEventHours)

				if memberAttrs["meetings"] < totalMeetings:

					DB_Manage.edit_attr("members", discordID, "meetings", totalMeetings)

			elif Functions.is_paid(memberObj):

				if memberAttrs["hours"] < totalEventHours:

					DB_Manage.edit_attr("members", discordID, "hours", totalEventHours)

			isActive = (float(memberAttrs["hours"]) >= totalEventHours/2) and (float(memberAttrs["meetings"]) >= totalMeetings/2)
			DB_Manage.edit_attr("members", discordID, "isActive", isActive)

	@tasks.loop(hours = 24)
	async def update_event_db(self):

		for eventName in DB_Manage.get_event_names():

			eventAttrs = DB_Manage.get_attrs("events", eventName)

			if (eventAttrs["start"] is not None) and (eventAttrs["end"] is not None):

				DB_Manage.edit_attr("events", eventName, "duration", eventAttrs["end"] - eventAttrs["start"])

			if (eventAttrs["isMeeting"] == 0) and (eventAttrs["end"] is None) and (time_now() - eventAttrs["start"] > 24 * 60 * 60):

				DB_Manage.edit_attr("events", eventName, "end", time_now())
				DB_Manage.edit_attr("events", eventName, "duration", eventAttrs["end"] - eventAttrs["start"])

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.strip_after_prefix = True

		# self.tngServerID = 1014692801281273868
		self.tngServerID = 1333588190782816367 # TEST SERVER ID

		self.activeEvents = {}

	async def on_ready(self):

		pass

	async def on_command_error(self, ctx, error):

		errorType = str(type(error))

		await ctx.send(f"There was a problem:\n\n`{errorType}`: {error}")

	# def command(self, *args, **kwargs):
	#
	#     def decorator(function):
	#
	#         newCommand = commands.core.Command(function)
	#         self.add_command(newCommand)
	#
	#         return newCommand
	#
	#     return decorator