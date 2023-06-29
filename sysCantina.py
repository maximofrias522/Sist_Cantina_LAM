import sqlite3
import uuid 
import kivi

def generate_unique_id():
    unique_id1 = str(uuid.uuid4()). replace('-', '')
    unique_id = unique_id1[:20]
    return unique_id

conn = sqlite3.connect('DBCantina.db')
c = conn.cursor()

c.execute(' ')