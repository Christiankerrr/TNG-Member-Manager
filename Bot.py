from discord.ext import commands, tasks

class BotClient (commands.Bot):

	@tasks.loop(hours = 24)
	def update_member_db(self):

		pass

	@tasks.loop(hours = 24)
	def prune_events(self):

		pass

	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		self.strip_after_prefix = True

		self.activeEvents = []

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