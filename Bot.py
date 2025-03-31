from discord.ext import commands, tasks

from DB_Manage import get_total_hours, get_total_meetings, get_all_ids, get_attrs, edit_attr

class BotClient (commands.Bot):

	@tasks.loop(hours = 24)
	async def update_member_db(self):

		tngServer = self.get_guild(self.tngServerID)

		totalEventHours = get_total_hours()
		totalMeetings = get_total_meetings()

		for id in get_all_ids():

			memberAttrs = get_status(id)

			memberObj = tngServer.fetch_member(id)
			edit_attr("members", id, "tag", memberObj.name)
			edit_attr("members", id, "name", memberObj.nick)

			isActive = (memberAttrs["hours"] >= totalEventHours/2) and (memberAttrs["meeting"] >= totalMeetings/2)
			edit_attr("isActive", isActive)

	@tasks.loop(hours = 24)
	async def prune_events(self):

		for event in self.activeEvents:

			pass

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.strip_after_prefix = True

		self.tngServerID = 1014692801281273868

		self.activeEvents = []
		self.registrationInfo = {}

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