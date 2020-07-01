import sqlite3

conn = sqlite3.connect('we.db', check_same_thread=False)

def get_conn():
    return conn

def close_conn():
    conn.close()
    
def init_db():
    # Get connection
    conn = get_conn()
    cursor = conn.cursor()

    # Drop if there's existing table
    try:
        cursor.execute('''DROP TABLE games;''')
    except:
        pass

    # Create table
    cursor.execute('''CREATE TABLE games
                    (
                        id integer NOT NULL PRIMARY KEY,
                        name text NOT NULL,
                        location text NOT NULL,
                        city text NOT NULL,
                        product_code text NOT NULL,
                        url text NOT NULL
                    )''')

    # Commit
    conn.commit()