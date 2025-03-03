# FOR MY PYCHARM PEEPS -Matt
# import pip
#
# pip.main(["install", "discord", "pymysql"])

from Commands import bot
from Event import start_event, end_event, start_meeting

# with open("Token.txt") as file:
#
# 	token = file.readline()
# 	bot.run(token)

event = start_event(title = "Test Event")

print(event)

end_event(event)

event.add_attendee(attendeeName = "Matthew Karten")

print(event)

meeting = start_meeting()

print(meeting)

end_event(meeting)

print(meeting)