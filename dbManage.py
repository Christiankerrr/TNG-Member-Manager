# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management

# QUESTION: DO WE NEED A SETTER FOR EVERY MEMBER ATTRIBUTE?

import pymysql

# Temporary example code (REMOVE LATER)
#
#new_member = Member("001", "tag1", "John Doe", "Vegan", "L", "M", "Member", 10, 2, 5, 1, 1)
#writeMember(new_member)
#
#new_event = Event("Team Meeting", "2025-02-25 14:00:00", "2025-02-25 15:00:00", 60, ["person", "second", "third"])
#writeEvent(new_event)

# Establish connection
# OUTPUT: database and cursor
def get_Connection():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="se300",
            database="memberdb"
        )
        return tngDB, tngDB.cursor()
    except pymysql.MySQLError as err:
        print(f"Database Connection Error: {err}")
        return None, None

# Create new database
def create_Database():
    try:
        # Connect to MySQL server
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="se300"
        )
        cursor = tngDB.cursor()

        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0].lower() for db in cursor.fetchall()]

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

        print("Tables created successfully")

    except pymysql.MySQLError as err:
        print(f"Error: {err}")

# Add a member
# INPUT: Member object
def write_Member(newMember):
    tngDB, cursor = get_Connection()
    if not tngDB or not cursor:
        return

    try:
        # Check if member already exists by ID or tag
        cursor.execute("SELECT COUNT(*) FROM members WHERE id = %s OR tag = %s", (newMember.id, newMember.tag))
        if cursor.fetchone()[0] > 0:
            print(f"Member with ID {newMember.id} or Tag {newMember.tag} already exists.")
            return

        # Proceed with adding the member if not already in database
        query = """
            INSERT INTO members (id, tag, nme, diet, sze, cut, pos, points_spent, coupons, meetings, hours, is_active, is_trained) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            newMember.id, newMember.tag, newMember.nme, newMember.diet,
            newMember.sze, newMember.cut, newMember.pos,
            newMember.points_spent, newMember.coupons, newMember.meetings,
            newMember.hours, newMember.is_active, newMember.is_trained
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
def write_Event(newEvent):
    tngDB, cursor = get_Connection()
    if not tngDB or not cursor:
        return

    try:
        query = """
            INSERT INTO events (title, start, end, duration, attendees) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            newEvent.title, newEvent.start, newEvent.end,
            newEvent.duration, ",".join(newEvent.attendees) if isinstance(newEvent.attendees, list) else newEvent.attendees
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
def remove_Member(memberID):
    tngDB, cursor = get_Connection()
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
def update_Tag(memberID, newTag):
    tngDB, cursor = get_Connection()
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
def update_Name(memberID, newName):
    tngDB, cursor = get_Connection()
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
def update_Diet(memberID, newDiet):
    tngDB, cursor = get_Connection()
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
def update_Size(memberID, newSize):
    tngDB, cursor = get_Connection()
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
def update_Cut(memberID, newCut):
    tngDB, cursor = get_Connection()
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
def update_Position(memberID, newPos):
    tngDB, cursor = get_Connection()
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
def update_Points_Spent(memberID, pointsToAdd):
    tngDB, cursor = get_Connection()
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
def update_Coupons(memberID, couponsToAdd):
    tngDB, cursor = get_Connection()
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
def update_Meetings(memberID, meetingsToAdd):
    tngDB, cursor = get_Connection()
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
def update_Hours(memberID, newHours):
    tngDB, cursor = get_Connection()
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
def update_Training(memberID, isTrained):
    tngDB, cursor = get_Connection()
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
def get_Status(memberID):
    tngDB, cursor = get_Connection()
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
def get_Attendees(eventName):
    tngDB, cursor = get_Connection()
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

# Print member database to command line
def print_Members():
    tngDB, cursor = get_Connection()
    if not tngDB or not cursor:
        return

    try:
        # Retrieve all members from the database
        cursor.execute("SELECT * FROM members")
        results = cursor.fetchall()

        if results:
            # Get column headers
            column_headers = [desc[0] for desc in cursor.description]

            # Print column headers
            print("\t".join(column_headers))

            # Print each member's data in a readable format
            for row in results:
                print("\t".join(str(value) for value in row))
        else:
            print("No members found.")
            column_headers = [desc[0] for desc in cursor.description]
            print("\t".join(column_headers))

    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if tngDB:
            tngDB.close()

# Print event database to command line
def print_Events():
    tngDB, cursor = get_Connection()
    if not tngDB or not cursor:
        return

    try:
        # Retrieve all events from the database
        cursor.execute("SELECT * FROM events")
        results = cursor.fetchall()

        if results:
            # Get column headers
            column_headers = [desc[0] for desc in cursor.description]

            # Print column headers
            print("\t".join(column_headers))

            # Print each event's data in a readable format
            for row in results:
                print("\t".join(str(value) for value in row))
        else:
            print("No events found.")
            column_headers = [desc[0] for desc in cursor.description]
            print("\t".join(column_headers))

    except pymysql.MySQLError as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if tngDB:
            tngDB.close()