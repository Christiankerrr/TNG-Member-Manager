# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management

import pymysql

# Temporary example code (REMOVE LATER)
#
# new_member = Member("001", "tag1", "John Doe", "Vegan", "L", "M", "Member", 10, 2, 5, 1, 1)
# writeMember(new_member)
#
# new_event = Event("Team Meeting", "2025-02-25 14:00:00", "2025-02-25 15:00:00", 60, ["person", "second", "third"])
# writeEvent(new_event)

# Establish connection
# OUTPUT: database and cursor
def get_connection():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="memberdb"
        )
        return tngDB, tngDB.cursor()
    except pymysql.MySQLError as err:
        return None, None

# Create new database
def create_database():
    error = None
    tngDB = None
    cursor = None
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = tngDB.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0].lower() for db in cursor.fetchall()]
        if "memberdb" in databases:
            raise Exception("Database 'memberdb' already exists.")

		if "memberdb" not in databases:
			cursor.execute("CREATE DATABASE memberdb")
			print("Database created successfully")

		# Use the database
		cursor.execute("USE memberdb")

		# Create members table
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id VARCHAR(50) PRIMARY KEY, 
                tag VARCHAR(100), 
                nme VARCHAR(255), 
                diet TEXT,
                sze VARCHAR(50), 
                cut VARCHAR(50), 
                pos VARCHAR(100), 
                points_spent INT DEFAULT 0,
                coupons INT DEFAULT 0, 
                meetings INT DEFAULT 0, 
                hours INT DEFAULT 0,
                is_active TINYINT(1) DEFAULT 1, 
                is_trained TINYINT(1) DEFAULT 0
            )
        """)

		# Create events table
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                title VARCHAR(255), 
                start DATETIME, 
                end DATETIME, 
                duration INT,
                attendees TEXT
            )
        """)
    except Exception as err:
        error = err
    finally:
        if cursor is not None:
            cursor.close()
        if tngDB is not None:
            tngDB.close()
        if error is not None:
            raise error

# Delete database
# UPDATE MYSQL PASSWORD HERE
# INPUT: name of database
def delete_database(dbName):
    error = None
    tngDB = None
    cursor = None
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = tngDB.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0].lower() for db in cursor.fetchall()]
        if dbName.lower() in databases:
            cursor.execute(f"DROP DATABASE {dbName}")
            tngDB.commit()
        else:
            error = Exception(f"Database '{dbName}' does not exist.")
    except Exception as err:
        error = err
    finally:
        if cursor is not None:
            cursor.close()
        if tngDB is not None:
            tngDB.close()
        if error is not None:
            raise error

# Add a member to the member database
# INPUT: id, tag, name, other values can be defaults
def write_member(memberID, newTag, name, diet=None, size=None, cut=None,
                 position="Member", points_spent=0, coupons=0,
                 meetings=0, hours=0, is_trained=False):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM members WHERE id = %s OR tag = %s",
            (memberID, newTag)
        )
        if cursor.fetchone()[0] > 0:
            error = Exception(f"Member with ID {memberID} or Tag {newTag} already exists.")
        query = """
            INSERT INTO members (
                id, tag, name, diet, size, cut, pos, points_spent,
                coupons, meetings, hours, is_active, is_trained
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s)
        """
		values = (
			newMember.discordID, newMember.discordTag, newMember.name, newMember.diet,
			newMember.size, newMember.cut, newMember.position,
			newMember.pointsSpent, newMember.coupons, newMember.meetings,
			newMember.hours, newMember.isActive, newMember.isTrained
			)
		cursor.execute(query, values)
		tngDB.commit()
		print("Member added successfully.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Add an event
# INPUT: Event object
def write_event(newEvent):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		query = """
            INSERT INTO events (title, start, end, duration, attendees) 
            VALUES (%s, %s, %s, %s, %s)
        """
		values = (
			newEvent.title, newEvent.start, newEvent.end,
			newEvent.duration,
			",".join(newEvent.attendees) if isinstance(newEvent.attendees, list) else newEvent.attendees
			)
		cursor.execute(query, values)
		tngDB.commit()
		print("Event added successfully.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		cursor.close()
		tngDB.close()

# Remove a member from the database
# INPUT: member ID
def remove_member(memberID):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		query = "DELETE FROM members WHERE id = %s"
		cursor.execute(query, (memberID,))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' removed successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

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

# Calculate if a member is active or not HOW DO WE DO THIS
# INPUT: member ID

# Update if a member is trained or not
# INPUT: member ID and trained bool
def update_training(memberID, isTrained):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return

	try:

		# Update the member's is_trained status
		query = "UPDATE members SET is_trained = %s WHERE id = %s"
		cursor.execute(query, (isTrained, memberID))
		tngDB.commit()

		if cursor.rowcount > 0:

			print(f"Member with ID '{memberID}' training status updated successfully.")

		else:

			print(f"No member found with ID '{memberID}'.")

	except pymysql.MySQLError as err:

		print(f"Error: {err}")

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Get a member's status
# INPUT: member ID
# OUTPUT: dictionary with member info
def get_status(memberID):
	tngDB, cursor = get_connection()
	if not tngDB or not cursor:
		return None

	try:

		# Retrieve all data for the member based on the ID
		cursor.execute("SELECT * FROM members WHERE id = %s", (memberID,))
		result = cursor.fetchone()

		if result:

			# Get column headers (the column names)
			column_headers = [desc[0] for desc in cursor.description]

			# Create a dictionary with column headers as keys and member data as values
			member_data = dict(zip(column_headers, result))

			return member_data

		else:

			print(f"No member found with ID: {memberID}")
			return None

	except pymysql.MySQLError as err:

		print(f"Error: {err}")
		return None

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
	if not tngDB or not cursor:
		return None

	try:

		# Retrieve the attendees of the event based on the event title
		cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
		result = cursor.fetchone()

		if result:

			# Convert the comma-separated string of attendees into a list
			attendees = result[0].split(",") if result[0] else []
			return attendees

		else:

			print(f"No event found with title: {eventName}")
			return None

	except pymysql.MySQLError as err:

		print(f"Error: {err}")
		return None

	finally:

		if cursor:
			cursor.close()

		if tngDB:
			tngDB.close()

# Get the member table as a string
# OUTPUT: string with table
def print_members():
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Error: Unable to connect to the database."

    try:
        # Retrieve all members from the database
        cursor.execute("SELECT * FROM members")
        results = cursor.fetchall()

        if results:
            # Get column headers
            column_headers = [desc[0] for desc in cursor.description]

            # Format the data as a string
            output = ["\t".join(column_headers)]
            output.extend("\t".join(str(value) for value in row) for row in results)

            return "\n".join(output)
        else:
            return "No members found."

    except pymysql.MySQLError as err:
        return f"Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if tngDB:
            tngDB.close()
