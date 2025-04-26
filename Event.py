class Event:

	def __init__(self, title, startTime):

		self.title = title
		self.startTime = startTime

class Meeting(Event):

	def __init__(self, attendees = ()):

		timeNow = time.time()
		timeObj = time.localtime(timeNow)
		title = time.strftime("%m/%d/%Y Member Meeting", timeObj)

		super().__init__(title, start = None, end = None, attendees = attendees)