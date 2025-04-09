# I CHANGED THIS FILE

import math
import time

def start_event(title):

	return Event(title)

def start_meeting():

	return Meeting()

def end_event(eventObj):

	if type(eventObj) is Meeting:

		return

	eventObj.end = time.time()
	for attendee in eventObj.attendees:

		# Do logic to sign members out
		pass

class Event:

	def __init__(self, title, start = time.time(), end = None, attendees = ()):

		self.title = title
		self.start = start
		self.end = end
		self.attendees = attendees

	def __str__(self):

		if self.start is not None:

			startObj = time.localtime(self.start)
			startStr = time.strftime("%B %d, %Y %I:%M:%S %p", startObj)

		else:

			startStr = "None"

		if self.end is not None:

			endObj = time.localtime(self.end)
			endStr = time.strftime("%B %d, %Y %I:%M:%S %p", endObj)

		else:

			endStr = "None"

		# if self.duration is not None:
		#
		# 	hours = self.duration // 3600
		# 	seconds = math.floor(self.duration % 60)
		# 	minutes =
		# 	durationObj = time.localtime(self.duration)
		# 	durationStr = time.strftime("%H:%M:%S", durationObj)
		#
		# else:
		#
		# 	durationStr = "None"

		attendees = self.attendees if len(self.attendees) > 0 else [None]

		strLines = [
			f"-- \"{self.title}\" Event Description --",
			"",
			f"\tStart Time: {startStr}",
			f"\tEnd Time: {endStr}",
			f"\tDuration: {self.duration} s",
			"",
			"\tAttendees:",
			*[f"\t\t{name}" for name in attendees],
			""
		]

		return "\n".join(strLines)

	@property
	def duration(self):

		if self.start is not None and self.end is not None:

			return self.end - self.start

		else:

			return None

	def add_attendee(self, attendeeName):

		self.attendees = self.attendees + (attendeeName,)

class Meeting (Event):

	def __init__(self, attendees = ()):

		timeNow = time.time()
		timeObj = time.localtime(timeNow)
		title = time.strftime("%m/%d/%Y Member Meeting", timeObj)

		super().__init__(title, start = None, end = None, attendees = attendees)