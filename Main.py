## WELCOME TO THE DISCORD BOT ##
import DB_Menu
import asyncio

from Commands import bot

bot.remove_command('help')

async def load():
	await bot.load_extension("cogs.help")

async def main():
	async with bot:
		await load()
		
		await bot.start("")

asyncio.run(main())