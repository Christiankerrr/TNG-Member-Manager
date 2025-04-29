# Touch-N-Go Member Manager
# Adrian Fanjoy
# Code graveyards

# Update a member's tag
# INPUT: member ID and new tag
def update_tag(memberID, newTag):
	tngDB, cursor = get_connection()

	if not tngDB or not cursor:
		return

	try:

		# Update the member's tag
		query = "UPDATE members SET tag = %s WHERE id = %s"
		cursor.execute(query, (newTag, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' tag updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's name
# INPUT: member ID and new name
def update_name(memberID, newName):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's name
		query = "UPDATE members SET nme = %s WHERE id = %s"
		cursor.execute(query, (newName, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' name updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's diet
# INPUT: member ID and new diet
def update_diet(memberID, newDiet):
	tngDB, cursor = get_connection()

	if not tngDB or not cursor:
		return

	try:

		# Update the member's diet
		query = "UPDATE members SET diet = %s WHERE id = %s"
		cursor.execute(query, (newDiet, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' diet updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's shirt size
# INPUT: member ID and new size
def update_size(memberID, newSize):
	tngDB, cursor = get_connection()

	if not tngDB or not cursor:
		return

	try:

		# Update the member's shirt size
		query = "UPDATE members SET sze = %s WHERE id = %s"
		cursor.execute(query, (newSize, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' shirt size updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's shirt cut
# INPUT: member ID and new cut
def update_cut(memberID, newCut):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's cut
		query = "UPDATE members SET cut = %s WHERE id = %s"
		cursor.execute(query, (newCut, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' cut updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's position
# INPUT: member ID and new position
def update_position(memberID, newPos):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's position
		query = "UPDATE members SET pos = %s WHERE id = %s"
		cursor.execute(query, (newPos, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' position updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's spent points
# INPUT: member ID and number of points to add
def update_points_spent(memberID, pointsToAdd):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's points spent
		query = "UPDATE members SET points_spent = points_spent + %s WHERE id = %s"
		cursor.execute(query, (pointsToAdd, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' spent points updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a members coupons
# INPUT: member ID and number of coupons to add
def update_coupons(memberID, couponsToAdd):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's coupons
		query = "UPDATE members SET coupons = coupons + %s WHERE id = %s"
		cursor.execute(query, (couponsToAdd, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' coupons updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's number of meetings
# INPUT: member ID and number of meetings to add
def update_meetings(memberID, meetingsToAdd):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's number of meetings
		query = "UPDATE members SET meetings = meetings + %s WHERE id = %s"
		cursor.execute(query, (meetingsToAdd, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' meetings updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Update a member's hours
# INPUT: member's ID and hours to add
def update_hours(memberID, newHours):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Retrieve current hours for the member
		cursor.execute("SELECT hours FROM members WHERE id = %s", (memberID,))
		result = cursor.fetchone()

		if result:

			currHours = result[0]
			totHours = currHours + newHours

			# Update the member's hours in the database
			query = "UPDATE members SET hours = %s WHERE id = %s"
			cursor.execute(query, (totHours, memberID))
			tngDB.commit()

			print(f"Member hours updated. New hours: {totHours}")

		else:

			print(f"No member found with ID: {memberID}")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Get the list of all members who attended an event
# INPUT: event name
# OUTPUT: event attendees
def get_attendees(eventName):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if result:
            attendees = result[0].split(",") if result[0] else []
            if attendees:
                return ", ".join(attendees)
            else:
                error = Exception("No attendees found.")
        else:
            error = Exception(f"Error: No event found with title '{eventName}'.")
    except Exception as err:
            error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error
		

## Jacob's Additions: 4/25/2025
@bot.command()
async def shit_pants(ctx):

	raise Exception("NOOOOOOOOO")
shit_pants.adminOnly = False

@bot.command()
async def surveyverify(ctx):
    embed = discord.Embed(
        title="Welcome to the TNG Discord",
        description="Click the button below to provide information for all TNG Events.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=VerifyView())
surveyverify.adminOnly = False

@bot.command()
async def write_member(ctx, memberID, memberTag, memberName):

	DB_Manage.write_member(memberID, memberTag, memberName)
write_member.adminOnly = True