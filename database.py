import sqlite3

def init_db():
    # SQLite automatic database file create karega
    conn = sqlite3.connect('kisanpro_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS farmer_groups 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, total_acres REAL, total_farmers INTEGER, crop TEXT, near_mill TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def save_group(group_name, total_acres, total_farmers, crop, near_mill, status):
    conn = sqlite3.connect('kisanpro_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO farmer_groups (group_name, total_acres, total_farmers, crop, near_mill, status) VALUES (?, ?, ?, ?, ?, ?)",
              (group_name, total_acres, total_farmers, crop, near_mill, status))
    conn.commit()
    conn.close()

def get_all_groups():
    conn = sqlite3.connect('kisanpro_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM farmer_groups")
    rows = c.fetchall()
    conn.close()
    return rows