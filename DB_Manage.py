# I CHANGED THIS FILE

# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management

import pymysql
from datetime import datetime

# Establish connection
# OUTPUT: database and cursor
def get_connection():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="data1013$",
            database="memberdb"
        )
        return tngDB, tngDB.cursor()
    except pymysql.MySQLError as err:
        return None, None

# Create new database
def create_database():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="data1013$"
        )
        cursor = tngDB.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0].lower() for db in cursor.fetchall()]
        if "memberdb" not in databases:
            cursor.execute("CREATE DATABASE memberdb")
        cursor.execute("USE memberdb")
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                title VARCHAR(255),
                start DATETIME,
                end DATETIME,
                duration INT,
                attendees TEXT,
                isMeeting TINYINT(1) DEFAULT 0
            )
        """)
        return "Database and tables initialized successfully."
    except pymysql.MySQLError as err:
        return f"Error: {err}"

# Add a member
# INPUT: id, tag, name, other values can be defaults
def write_member(member_id, tag, name, diet=None, size=None, cut=None, position="Member", points_spent=0, coupons=0, meetings=0, hours=0, is_trained=False):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT COUNT(*) FROM members WHERE id = %s OR tag = %s", (member_id, tag))
        if cursor.fetchone()[0] > 0:
            return f"Member with ID {member_id} or Tag {tag} already exists."
        query = """
            INSERT INTO members (id, tag, nme, diet, sze, cut, pos, points_spent, coupons, meetings, hours, is_active, is_trained) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s)
        """
        values = (member_id, tag, name, diet, size, cut, position, points_spent, coupons, meetings, hours, is_trained)
        cursor.execute(query, values)
        tngDB.commit()
        return "Member added successfully."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Add an event
# INPUT: title, start, end, all other values can be defaults
def write_event(title, start, end, duration=0, attendees="", isMeeting=1):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        query = """
            INSERT INTO events (title, start, end, duration, attendees, isMeeting) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (title, start, end, duration, attendees, isMeeting)
        cursor.execute(query, values)
        tngDB.commit()
        return "Event added successfully."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Remove a member from the database
# INPUT: member ID
def remove_member(memberID):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("DELETE FROM members WHERE id = %s", (memberID,))
        tngDB.commit()
        return "Member removed successfully." if cursor.rowcount > 0 else "No member found with the given ID."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Remove an event from the database
# INPUT: event name
def remove_event(eventName):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("DELETE FROM events WHERE title = %s", (eventName,))
        tngDB.commit()
        return "Event removed successfully." if cursor.rowcount > 0 else "No event found with the given name."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Edit the attributes of a member or event
# INPUT: mode, attribute name, new attribute value
def edit_attr(mode, recordIdentifier, attrName, newAttrVal):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        table = "members" if mode == "member" else "events"
        id_column = "id" if mode == "member" else "title"
        cursor.execute(f"DESCRIBE {table}")
        columns = [row[0] for row in cursor.fetchall()]
        if attrName not in columns:
            return f"Invalid attribute. Available attributes: {', '.join(columns)}"
        cursor.execute(f"UPDATE {table} SET {attrName} = %s WHERE {id_column} = %s", (newAttrVal, recordIdentifier))
        tngDB.commit()
        return "Attribute updated successfully." if cursor.rowcount > 0 else "No record found with the given identifier."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get attributes for member or event
# INPUT: member ID
# OUTPUT: dictionary with record info
def get_attrs(mode, recordIdentifier):
    tngDB, cursor = get_connection()
    try:
        table = "members" if mode == "member" else "events"
        id_column = "id" if mode == "member" else "title"

        cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (recordIdentifier,))
        result = cursor.fetchone()

        if result:
            column_headers = [desc[0] for desc in cursor.description]
            return dict(zip(column_headers, result))
        return f"No {mode} found with identifier: {recordIdentifier}"
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get the list of all members who attended an event
# INPUT: event name
# OUTPUT: event attendees
def get_attendees(eventName):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Error: Unable to connect to the database."
    try:
        cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if result:
            attendees = result[0].split(",") if result[0] else []
            return ", ".join(attendees) if attendees else "No attendees found."
        else:
            return f"Error: No event found with title '{eventName}'."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get all ids in the database
# OUTPUT: list of all ids as integers
def get_all_ids():
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT id FROM members")
        return [row[0] for row in cursor.fetchall()]
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get sum of hours from all events
# OUTPUT: string number of hours
def get_total_hours():
    tngDB, cursor = get_connection()
    try:
        cursor.execute("SELECT COALESCE(SUM(duration), 0) FROM events WHERE isMeeting = 0")
        total_hours = cursor.fetchone()[0]
        return total_hours
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get total number of meetings
# OUTPUT: string number of meetings
def get_total_meetings():
    tngDB, cursor = get_connection()
    try:
        cursor.execute("SELECT COUNT(*) FROM events WHERE isMeeting = 1")
        total_meetings = cursor.fetchone()[0]
        return total_meetings
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get all event names in the table
# OUTPUT: list of event names
def get_event_names():
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return []
    try:
        cursor.execute("SELECT title FROM events")
        return [row[0] for row in cursor.fetchall()]
    except pymysql.MySQLError as err:
        return []
    finally:
        cursor.close()
        tngDB.close()

# Get either table as a string
# OUTPUT: string with table
def print_table(mode):
    tngDB, cursor = get_connection()
    try:
        table = "members" if mode == "member" else "events"
        cursor.execute(f"SELECT * FROM {table}")
        results = cursor.fetchall()
        if results:
            column_headers = [desc[0] for desc in cursor.description]
            output = ["\t".join(column_headers)]
            output.extend("\t".join(str(value) for value in row) for row in results)
            return "\n".join(output)
        return f"No records found in {table}."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Determine if an event can be signed in to
# INPUT: name of the event
# OUTPUT: boolean
def can_signin(eventName):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return False
    try:
        cursor.execute("SELECT start, end FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if not result:
            return False

        startTime, endTime = result
        if not startTime or not endTime:
            return False

        current_time = datetime.now()
        return startTime <= current_time <= endTime
    except pymysql.MySQLError as err:
        return False
    finally:
        cursor.close()
        tngDB.close()

# Determine if an event can be registered for
# INPUT: name of the event
# OUTPUT: boolean
def can_register(eventName):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return False
    try:
        cursor.execute("SELECT start FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if not result:
            return False

        startTime = result[0]
        if not startTime:
            return False

        current_time = datetime.now()
        return current_time < startTime
    except pymysql.MySQLError as err:
        return False
    finally:
        cursor.close()
        tngDB.close()

# Add a member to the list of event attendees
# INPUT: event name and member ID
def add_attend(eventName, memberID):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if not result:
            return "Event not found."

        attendees = result[0]
        attendList = attendees.split(",") if attendees else []

        if memberID in attendList:
            return "Member is already an attendee."

        attendList.append(memberID)
        updatedAttend = ",".join(attendList)

        cursor.execute("UPDATE events SET attendees = %s WHERE title = %s", (updatedAttend, eventName))
        tngDB.commit()
        return "Member added to event attendees."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()
