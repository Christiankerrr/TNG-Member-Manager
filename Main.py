# FOR MY PYCHARM PEEPS -Matt
# import pip
#
# pip.main(["install", "discord", "pymysql", "cryptography"])

from os import getenv

from Commands import bot

if __name__ == "__main__":

	bot.run(getenv("TOKEN"))

