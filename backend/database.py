import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def _init_db():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS spaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            space_id INTEGER NOT NULL,
            FOREIGN KEY(space_id) REFERENCES spaces(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            space_id INTEGER NOT NULL,
            FOREIGN KEY(space_id) REFERENCES spaces(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            space_id INTEGER NOT NULL,
            FOREIGN KEY(space_id) REFERENCES spaces(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_space(name):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO spaces (name) VALUES (?)
    ''', (name,))
    conn.commit()
    conn.close()

def get_spaces():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM spaces
    ''')
    spaces = c.fetchall()
    conn.close()
    return spaces

def get_space(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM spaces WHERE id = ?
    ''', (space_id,))
    space = c.fetchone()
    conn.close()
    return space

def get_space_by_name(space_name):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM spaces WHERE name = ?
    ''', (space_name,))
    space = c.fetchone()
    conn.close()
    return space

def get_space_meetings(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM meetings WHERE space_id = ?
    ''', (space_id,))
    meetings = c.fetchall()
    conn.close()
    return meetings

def get_space_events(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM calendar_events WHERE space_id = ?
    ''', (space_id,))
    events = c.fetchall()
    conn.close()
    return events


def add_meeting(name, space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO meetings (name, space_id) VALUES (?, ?)
    ''', (name, space_id))
    conn.commit()
    conn.close()

def get_meetings(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM meetings WHERE space_id = ?
    ''', (space_id,))
    meetings = c.fetchall()
    conn.close()
    return meetings

def add_calendar_event(name, space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO calendar_events (name, space_id) VALUES (?, ?)
    ''', (name, space_id))
    conn.commit()
    conn.close()

def get_calendar_events(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM calendar_events WHERE space_id = ?
    ''', (space_id,))
    calendar_events = c.fetchall()
    conn.close()
    return calendar_events

def add_document(name, space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO documents (name, space_id) VALUES (?, ?)
    ''', (name, space_id))
    conn.commit()
    conn.close()

def get_documents(space_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM documents WHERE space_id = ?
    ''', (space_id,))
    documents = c.fetchall()
    conn.close()
    return documents

if __name__ == "__main__":
    # run to initialize the database
    _init_db()

    # optional: add some test data
    add_space("Test Space 1")
    add_space("Big Stepper")
    add_space("googlemhacks-hackthon")

    add_meeting("meeting with drake", 1)
    add_meeting("meeting with future", 1)
    add_meeting("midnight coding sesh", 3)

    add_calendar_event("event with drake", 2)
    add_calendar_event("event with future", 1)
    add_calendar_event("bodega brothers mashallah", 3)