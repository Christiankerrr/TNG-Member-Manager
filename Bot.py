from discord.ext import commands, tasks
from time import time as time_now

from DB_Manage import get_attrs, edit_attr, get_total_hours, get_total_meetings, get_all_ids, get_event_names

class BotClient (commands.Bot):

	@tasks.loop(hours = 24)
	async def update_member_db(self):

		tngServer = self.get_guild(self.tngServerID)

		totalEventHours = get_total_hours()
		totalMeetings = get_total_meetings()

		for discordID in get_all_ids():

			memberAttrs = get_attrs("members", discordID)

			memberObj = tngServer.fetch_member(discordID)
			edit_attr("members", discordID, "tag", memberObj.name)
			edit_attr("members", discordID, "name", memberObj.nick)

			memberRoleNames = [role.name for role in memberObj.roles]

			if "Executive Board" in memberRoleNames:

				if memberAttrs["hours"] < totalEventHours:

					edit_attr("members", discordID, "hours", totalEventHours)

				if memberAttrs["meetings"] < totalMeetings:

					edit_attr("members", discordID, "meetings", totalMeetings)

			elif "Paid Staff" in memberRoleNames:

				if memberAttrs["hours"] < totalEventHours:

					edit_attr("members", discordID, "hours", totalEventHours)

			isActive = (float(memberAttrs["hours"]) >= totalEventHours/2) and (float(memberAttrs["meetings"]) >= totalMeetings/2)
			edit_attr("members", discordID, "isActive", isActive)

	@tasks.loop(hours = 24)
	async def prune_events(self):

		for eventName in get_event_names():

			eventAttrs = get_attrs("events", eventName)

			if (eventAttrs["isMeeting"] == "False") and (time_now() - float(eventAttrs["startTime"]) > 24 * 60 * 60):

				edit_attr("events", eventName, "endTime", time_now())

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.strip_after_prefix = True

		self.tngServerID = 1014692801281273868

	async def on_ready(self):

		pass

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