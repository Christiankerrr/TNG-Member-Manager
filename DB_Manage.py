# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management functions

import pymysql
from time import time as time_now

# Establish connection
# UPDATE MYSQL PASSWORD HERE
# OUTPUT: database and cursor
def get_connection():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="MANunited1!1!1!",
            database="memberdb"
        )
        return tngDB, tngDB.cursor()
    except pymysql.MySQLError as err:
        return None, None

# Create new database
# UPDATE MYSQL PASSWORD HERE
def create_database():
    error = None
    tngDB = None
    cursor = None
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="MANunited1!1!1!"
        )
        cursor = tngDB.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0].lower() for db in cursor.fetchall()]
        if "memberdb" in databases:
            raise Exception("Database 'memberdb' already exists.")

        cursor.execute("CREATE DATABASE memberdb")
        cursor.execute("USE memberdb")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id VARCHAR(50) PRIMARY KEY,
                tag VARCHAR(100),
                name VARCHAR(255),
                diet TEXT,
                size VARCHAR(50),
                cut VARCHAR(50),
                pos VARCHAR(100),
                points_spent INT DEFAULT 0,
                coupons INT DEFAULT 0,
                meetings INT DEFAULT 0,
                hours FLOAT DEFAULT 0,
                is_active TINYINT(1) DEFAULT 1,
                is_trained TINYINT(1) DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                title VARCHAR(255),
                start DOUBLE PRECISION(20, 2),
                end DOUBLE PRECISION(20, 2),
                duration DOUBLE PRECISION(20, 2),
                attendees TEXT,
                isMeeting TINYINT(1) DEFAULT 0
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
            password="MANunited1!1!1!"
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
            memberID, newTag, name, diet, size, cut, position,
            points_spent, coupons, meetings, hours, is_trained
        )
        cursor.execute(query, values)
        tngDB.commit()
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Add an event to the event table
# INPUT: title and isMeeting, all other values can be defaults
def write_event(title, isMeeting, start=None, end=None, duration=0, attendees=""):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT COUNT(*) FROM events WHERE title = %s", (title,))
        if cursor.fetchone()[0] > 0:
            error = Exception(f"Event with title '{title}' already exists.")
        if start is not None and end is not None and end <= start:
            error = Exception("End time must be after start time.")

        if error is None:
            query = """
                INSERT INTO events (title, start, end, duration, attendees, isMeeting) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (title, start, end, duration, attendees, isMeeting)
            cursor.execute(query, values)
            tngDB.commit()
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Remove a member from the database
# INPUT: member ID
def remove_member(memberID):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("DELETE FROM members WHERE id = %s", (memberID,))
        tngDB.commit()
        if cursor.rowcount == 0:
            error = Exception("No record found with the given identifier.")
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Remove an event from the database
# INPUT: event name
def remove_event(eventName):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("DELETE FROM events WHERE title = %s", (eventName,))
        tngDB.commit()
        if cursor.rowcount == 0:
            error = Exception("No record found with the given identifier.")
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Edit the attributes of a member or event
# INPUT: mode, recordID (tag, ID, or name), attribute name, new attribute value
def edit_attr(mode, recordIdentifier, attrName, newAttrVal, forceEdit = False):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        # Check if in tuple format
        if attrName in ["diet", "attendees"] and isinstance(newAttrVal, tuple):
            if len(newAttrVal) != len(set(newAttrVal)):
                error = Exception(f"Duplicate entries found in {attrName}")
            newAttrVal = ",".join(str(item) for item in newAttrVal)

        # Check mode
        if mode not in ["members", "events"]:
            error = Exception("Invalid mode. Must be 'members' or 'events'.")

        # Check for attributes that cannot be modified
        if attrName == "isMeeting":
            error = Exception("Cannot modify 'isMeeting' attribute.")
        if attrName == "duration" and not forceEdit:
            error = Exception("Cannot modify 'duration' unless forceEdit is True.")

        # Set search variable
        if mode == "members":
            if isinstance(recordIdentifier, int):
                searchColumn = "id"
            else:
                searchColumn = "tag"
            table = "members"
        else:
            searchColumn = "title"
            table = "events"

        # Check to make sure tag is not duplicate
        if mode == "members" and attrName == "tag":
            cursor.execute("SELECT COUNT(*) FROM members WHERE tag = %s", (newAttrVal,))
            if cursor.fetchone()[0] > 0:
                error = Exception(f"Tag '{newAttrVal}' already exists")

        # Check to make sure end time is after start
        if mode == "events" and attrName == "end":
            cursor.execute("SELECT start FROM events WHERE title = %s", (recordIdentifier,))
            startTime = cursor.fetchone()
            if startTime and startTime[0] and newAttrVal <= startTime[0]:
                error = Exception("End time must be after start time")

        # Check that end time cannot be modified for meetings
        if mode == "events" and not forceEdit:
            cursor.execute(f"SELECT isMeeting FROM {table} WHERE title = %s", (recordIdentifier,))
            isMeeting = cursor.fetchone()
            if isMeeting and isMeeting[0] and attrName == "end":
                error = Exception("Cannot modify 'end' for a meeting unless forceEdit is True.")

        if error is None:
            cursor.execute(f"DESCRIBE {table}")
            columns = [row[0] for row in cursor.fetchall()]
            if attrName not in columns:
                error = Exception(f"Invalid attribute. Available attributes: {', '.join(columns)}")
            cursor.execute(
                f"UPDATE {table} SET {attrName} = %s WHERE {searchColumn} = %s",
                (newAttrVal, recordIdentifier)
            )
            tngDB.commit()
            if cursor.rowcount == 0:
                error = Exception("No record found with the given identifier.")
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get attributes for member or event
# INPUT: recordID (tag, ID, or name)
# OUTPUT: dictionary with record info
def get_attrs(mode, recordIdentifier):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        if mode == "members":
            if isinstance(recordIdentifier, int):
                searchColumn = "id"
            else:
                searchColumn = "tag"
            table = "members"
        else:
            searchColumn = "title"
            table = "events"

        cursor.execute(f"SELECT * FROM {table} WHERE {searchColumn} = %s", (recordIdentifier,))
        result = cursor.fetchone()
        if result:
            columnHeaders = [desc[0] for desc in cursor.description]
            recordDict = dict(zip(columnHeaders, result))

            if mode == "members" and recordDict.get("diet"):
                recordDict["diet"] = tuple(recordDict["diet"].split(','))

            if mode == "events" and recordDict.get("attendees"):
                attendees = recordDict["attendees"]
                if attendees:
                    recordDict["attendees"] = tuple(
                        attendee.strip()
                        for attendee in attendees.split(',')
                        if attendee.strip()
                    )
                else:
                    recordDict["attendees"] = tuple()
            return recordDict
        error = Exception(f"No {mode} found with identifier: {recordIdentifier}")
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get all ids in the database
# OUTPUT: list of all ids as integers
def get_all_ids():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT id FROM members")
        return [row[0] for row in cursor.fetchall()]
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get sum of hours from all events
# OUTPUT: number of hours
def get_total_hours():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT COALESCE(SUM(duration), 0) FROM events WHERE isMeeting = 0")
        totalHours = cursor.fetchone()[0]
        return totalHours
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get total number of meetings
# OUTPUT: number of meetings
def get_total_meetings():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT COUNT(*) FROM events WHERE isMeeting = 1")
        totalMeetings = cursor.fetchone()[0]
        return totalMeetings
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get all event names in the table
# OUTPUT: list of event names
def get_event_names():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    if not tngDB or not cursor:
        return []
    try:
        cursor.execute("SELECT title FROM events")
        return [row[0] for row in cursor.fetchall()]
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get either table as a string
# OUTPUT: string with table
def print_table(mode):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute(f"SELECT * FROM {mode}")
        results = cursor.fetchall()
        if results:
            columnHeaders = [desc[0] for desc in cursor.description]
            output = ["\t".join(columnHeaders)]
            output.extend("\t".join(str(value) for value in row) for row in results)
            return "\n".join(output)
        return f"No records found in {mode}."
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Determine if an event can be signed in to
# INPUT: name of the event
# OUTPUT: boolean
def can_sign_in(eventName):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT start, end FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if not result:
            return False

        startTime, endTime = result
        if not startTime or not endTime:
            return False

        currentTime = time_now()
        return startTime <= currentTime <= endTime
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Determine if an event can be registered
# INPUT: name of the event
# OUTPUT: boolean
def can_register(eventName):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT start FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if result is None:
            return False
        startTime = result[0]
        return startTime is None
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Add a member to the list of event attendees
# INPUT: event name and member ID
def add_attend(eventName, memberID):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT 1 FROM events WHERE title = %s", (eventName,))
        if not cursor.fetchone():
            raise Exception("Event not found.")

        cursor.execute("SELECT 1 FROM members WHERE id = %s", (memberID,))
        if not cursor.fetchone():
            raise Exception("Member not found.")

        cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        attendees = result[0] if result and result[0] else ""
        attendList = [str(x) for x in attendees.split(",")] if attendees else []

        if str(memberID) in attendList:
            raise Exception("Member is already an attendee.")

        attendList.append(str(memberID))
        updatedAttend = ",".join(attendList)
        cursor.execute("UPDATE events SET attendees = %s WHERE title = %s",
                       (updatedAttend, eventName))
        tngDB.commit()

    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Determine if a member exists in the database
# INPUT: member ID
# OUTPUT: boolean
def locate_member(memberID):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT 1 FROM members WHERE id = %s LIMIT 1", (str(memberID),))
        return cursor.fetchone() is not None
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Determine if a member exists in the database
# INPUT: member ID
# OUTPUT: boolean
def locate_event(eventName):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT 1 FROM events WHERE id = %s LIMIT 1", (str(eventName),))
        return cursor.fetchone() is not None
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Determine if a member is missing any data (size, cut, diet)
# INPUT: member ID
# OUTPUT: boolean if missing data, name of any missing attributes
def missing_data(memberID):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute(
            "SELECT diet, size, cut FROM members WHERE id = %s",
            (memberID,)
        )
        data = cursor.fetchone()
        if not data:
            error = Exception(f"No member found with ID: {memberID}")

        diet, size, cut = data
        dietMissing = not diet or not diet.strip()
        sizeMissing = not size or not size.strip()
        cutMissing = not cut or not cut.strip()
        return dietMissing, sizeMissing, cutMissing

    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error