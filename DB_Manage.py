# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management

import pymysql
from time import time as time_now

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
    error = None
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
                start FLOAT,
                end FLOAT,
                duration FLOAT,
                attendees TEXT,
                isMeeting TINYINT(1) DEFAULT 0
            )
        """)
    except Exception as err:
        error = err
    finally:
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
# INPUT: title, all other values can be defaults
def write_event(title, start=None, end=None, duration=0, attendees="", isMeeting=1):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
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
# INPUT: mode, attribute name, new attribute value
def edit_attr(mode, recordIdentifier, attrName, newAttrVal):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        if attrName in ["diet", "attendees"] and isinstance(newAttrVal, list):
            newAttrVal = str(newAttrVal)

        id_column = "id" if mode == "member" else "title"
        cursor.execute(f"DESCRIBE {mode}")
        columns = [row[0] for row in cursor.fetchall()]
        if attrName not in columns:
            error = Exception(f"Invalid attribute. Available attributes: {', '.join(columns)}")
        cursor.execute(
            f"UPDATE {mode} SET {attrName} = %s WHERE {id_column} = %s",
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
# INPUT: member ID
# OUTPUT: dictionary with record info
def get_attrs(mode, recordIdentifier):
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        table = "members" if mode == "member" else "events"
        id_column = "id" if mode == "member" else "title"

        cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (recordIdentifier,))
        result = cursor.fetchone()
        if result:
            column_headers = [desc[0] for desc in cursor.description]
            return dict(zip(column_headers, result))
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
# OUTPUT: string number of hours
def get_total_hours():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT COALESCE(SUM(duration), 0) FROM events WHERE isMeeting = 0")
        total_hours = cursor.fetchone()[0]
        return total_hours
    except Exception as err:
        error = err
    finally:
        cursor.close()
        tngDB.close()
        if error is not None:
            raise error

# Get total number of meetings
# OUTPUT: string number of meetings
def get_total_meetings():
    tngDB, cursor = get_connection()
    error = None
    if not tngDB or not cursor:
        error = Exception("Database connection error.")
    try:
        cursor.execute("SELECT COUNT(*) FROM events WHERE isMeeting = 1")
        totMeet = cursor.fetchone()[0]
        return totMeet
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
            column_headers = [desc[0] for desc in cursor.description]
            output = ["\t".join(column_headers)]
            output.extend("\t".join(str(value) for value in row) for row in results)
            return "\n".join(output)
        error = Exception("No records found in {mode}.")
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

        current_time = time_now()
        return startTime <= current_time <= endTime
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
        cursor.execute("SELECT attendees FROM events WHERE title = %s", (eventName,))
        result = cursor.fetchone()
        if not result:
            error = Exception("Event not found.")

        attendees = result[0]
        attendList = attendees.split(",") if attendees else []

        if memberID in attendList:
            error = Exception("Member is already an attendee.")

        attendList.append(memberID)
        updatedAttend = ",".join(attendList)

        cursor.execute("UPDATE events SET attendees = %s WHERE title = %s", (updatedAttend, eventName))
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