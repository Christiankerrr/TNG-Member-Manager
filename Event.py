import time

def start_event(title):

	return Event(title)

def start_meeting():

	return Meeting()

def end_event(eventObj):

	if type(eventObj) is Meeting:

		return

	eventObj.endTime = time.time()
	for attendee in eventObj.attendeeList:

		# Do logic to sign members out
		pass

class Event:

	def __init__(self, title, startTime = time.time(), endTime = None, attendeeList = ()):

		self.title = title
		self.startTime = startTime
		self.endTime = endTime
		self.attendeeList = attendeeList

	def __str__(self):

		if self.startTime is not None:

			startTimeObj = time.localtime(self.startTime)
			startTimeStr = time.strftime("%B %d, %Y %I:%M:%S %p", startTimeObj)

		else:

			startTimeStr = "None"

		if self.endTime is not None:

			endTimeObj = time.localtime(self.endTime)
			endTimeStr = time.strftime("%B %d, %Y %I:%M:%S %p", endTimeObj)

		else:

			endTimeStr = "None"

		attendeeList = self.attendeeList if len(self.attendeeList) > 0 else [None]

		strLines = [
			f"-- \"{self.title}\" Event Description --",
			"",
			f"\tStart Time: {startTimeStr}",
			f"\tEnd Time: {endTimeStr}",
			"",
			"\tAttendees:",
			*[f"\t\t{name}" for name in attendeeList],
			""
		]

		return "\n".join(strLines)

	def add_attendee(self, attendeeName):

		self.attendeeList = self.attendeeList + (attendeeName,)

class Meeting (Event):

	def __init__(self, attendeeList = ()):

		timeNow = time.time()
		timeObj = time.localtime(timeNow)
		title = time.strftime("%m/%d/%Y Member Meeting", timeObj)

		super().__init__(title, startTime = None, endTime = None, attendeeList = attendeeList)