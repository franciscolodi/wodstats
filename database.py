import sqlite3
import datetime

def save_prediction(user, comp, data, pred):

    conn = sqlite3.connect("logs.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            user TEXT,
            competition TEXT,
            W1T REAL,
            W2T REAL,
            W3T REAL,
            W4R REAL,
            W5AR REAL,
            W5BL REAL,
            prediction REAL,
            date TEXT
        )
    """)

    c.execute("""
        INSERT INTO predictions VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        user,
        comp,
        data["W1T"],
        data["W2T"],
        data["W3T"],
        data["W4R"],
        data["W5AR"],
        data["W5BL"],
        pred,
        str(datetime.datetime.now())
    ))

    conn.commit()
    conn.close()
