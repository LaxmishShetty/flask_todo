import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("INSERT INTO tasks (title, content) VALUES (?, ?)",
            ('DSA', 'Practice arrays ')
            )


cur.execute("INSERT INTO tasks (title, content) VALUES (?, ?)",
            ('System Design', 'Practice system design concepts such as sharding, latency etc ')
            )

conn.commit()
conn.close()