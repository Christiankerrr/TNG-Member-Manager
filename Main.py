## WELCOME TO THE DISCORD BOT ##

import asyncio
import os

from Commands import bot
import DB_Menu

# bot.run(os.getenv("TOKEN"))

DB_Menu.run_menu()

bot.remove_command('help')

async def load():
	await bot.load_extension("cogs.help")

async def main():
	async with bot:
		await load()

		await bot.start("")

asyncio.run(main())