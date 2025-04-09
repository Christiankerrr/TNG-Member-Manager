# FOR MY PYCHARM PEEPS -Matt
# import pip
#
# pip.main(["install", "discord", "pymysql"])

import os

from Commands import bot

if __name__ == "__main__":

	bot.run(os.getenv("TOKEN"))

