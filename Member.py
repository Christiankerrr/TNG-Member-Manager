# I CHANGED THIS FILE

class Member:

	def __init__(self, discordID, discordTag, name, diet = None, size = None, cut = None, position = "Member", pointsSpent = 0, coupons = 0, meetings = 0, hours = 0, isTrained = False):

		self.discordID = discordID
		self.discordTag = discordTag
		self.name = name
		self.diet = diet
		self.size = size
		self.cut = cut
		self.position = position
		self.pointsSpent = pointsSpent
		self.coupons = coupons
		self.meetings = meetings
		self.hours = hours
		self.isTrained = isTrained

	def __str__(self):

		return str(self.__dict__)

	@property
	def isActive(self):

		# IDK boss
		pass

	def edit_attr(self, attrName, newAttrVal):

		objDict = self.__dict__
		if attrName in objDict.keys():

			objDict[attrName] = newAttrVal

		else:

			raise KeyError(f"Not a valid attribute of a member object (Valid attributes: {list(objDict.keys())})")
