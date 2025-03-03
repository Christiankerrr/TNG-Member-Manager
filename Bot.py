from discord.ext import commands

class BotClient(commands.Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.strip_after_prefix = True

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