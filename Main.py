# FOR MY PYCHARM PEEPS -Matt
# import pip
#
# pip.main(["install", "discord", "pymysql"])

import os
import time

from Commands import bot
from Event import start_event, end_event, start_meeting
from Member import Member

if __name__ == "__main__":

	bot.run("BotToken")
	
# with open("Token.txt") as file:
#
# 	token = file.readline()
# 	bot.run(token)

