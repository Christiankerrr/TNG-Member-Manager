# Touch-N-Go Member Manager
# Adrian Fanjoy
# Database management

import pymysql

# Establish connection
# OUTPUT: database and cursor
def get_connection():
    try:
        tngDB = pymysql.connect(
            host="localhost",
            user="root",
            password="se300",
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
            password="se300"
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
                attendees TEXT
            )
        """)
        return "Database and tables initialized successfully."
    except pymysql.MySQLError as err:
        return f"Error: {err}"

# Add a member
# INPUT: Member object
def write_member(newMember):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT COUNT(*) FROM members WHERE id = %s OR tag = %s", (newMember.discordID, newMember.discordTag))
        if cursor.fetchone()[0] > 0:
            return f"Member with ID {newMember.discordID} or Tag {newMember.discordTag} already exists."
        query = """
            INSERT INTO members (id, tag, nme, diet, sze, cut, pos, points_spent, coupons, meetings, hours, is_active, is_trained) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            newMember.discordID, newMember.discordTag, newMember.name, newMember.diet,
            newMember.size, newMember.cut, newMember.position,
            newMember.pointsSpent, newMember.coupons, newMember.meetings,
            newMember.hours, newMember.isActive, newMember.isTrained
        )
        cursor.execute(query, values)
        tngDB.commit()
        return "Member added successfully."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
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

# Edit the attributes of a member or event
# INPUT: attribute name, new attribute value, mode
def edit_attr(recordID, attrName, newAttrVal, mode):
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
        cursor.execute(f"UPDATE {table} SET {attrName} = %s WHERE {id_column} = %s", (newAttrVal, recordID))
        tngDB.commit()
        return "Attribute updated successfully." if cursor.rowcount > 0 else "No record found with the given ID."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get a member's status
# INPUT: member ID
# OUTPUT: dictionary with member info
def get_status(memberID):
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection failed."
    try:
        cursor.execute("SELECT * FROM members WHERE id = %s", (memberID,))
        result = cursor.fetchone()
        if result:
            column_headers = [desc[0] for desc in cursor.description]
            return dict(zip(column_headers, result))
        return f"No member found with ID: {memberID}"
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
def get_all_id():
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

# Get attributes for task loop update
# OUTPUT: total number of meetings, total event hours, all member ID's, amount of hours, amount of meetings
def get_loop_vals():
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(duration) FROM events")
        total_duration = cursor.fetchone()[0] or 0

        cursor.execute("SELECT id, hours, meetings FROM members")
        member_data = {row[0]: {"hours": row[1], "meetings": row[2]} for row in cursor.fetchall()}

        return total_events, total_duration, member_data
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()

# Get the member table as a string MAKE ONE FUNCTION AND ATTRIBUTE TO SELECT WHICH TABLE
# OUTPUT: string with table
def print_members():
    tngDB, cursor = get_connection()
    if not tngDB or not cursor:
        return "Database connection error."
    try:
        cursor.execute("SELECT * FROM members")
        results = cursor.fetchall()
        if results:
            column_headers = [desc[0] for desc in cursor.description]
            output = ["\t".join(column_headers)]
            output.extend("\t".join(str(value) for value in row) for row in results)
            return "\n".join(output)
        return "No members found."
    except pymysql.MySQLError as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        tngDB.close()