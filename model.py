import sqlite3

class InventoryModel:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY, name TEXT, barcode TEXT UNIQUE, quantity INTEGER, qr_code TEXT)''')
        self.conn.commit()

    def add_item(self, name, barcode, quantity, qr_code):
        try:
            self.c.execute("INSERT INTO items (name, barcode, quantity, qr_code) VALUES (?, ?, ?, ?)",
                      (name, barcode, quantity, qr_code))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_items(self):
        self.c.execute("SELECT * FROM items")
        return self.c.fetchall()

