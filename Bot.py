from discord.ext import commands, tasks

from DB_Manage import get_loop_vals, get_all_id, get_status, edit_attr

class BotClient (commands.Bot):

	@tasks.loop(hours = 24)
	async def update_member_db(self):

		tngServer = self.get_guild(self.tngServerID)

		totalEventHours, totalMeetings = get_loop_vals()

		for id in get_all_id():

			memberAttrs = get_status(id)

			memberObj = tngServer.fetch_member(id)
			edit_attr("tag", memberObj.name)
			edit_attr("name", memberObj.nick)

			isActive = (memberAttrs["hours"] >= totalEventHours/2) and (memberAttrs["meeting"] >= totalMeetings/2)
			edit_attr("isActive", isActive)

	@tasks.loop(hours = 24)
	async def prune_events(self):

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