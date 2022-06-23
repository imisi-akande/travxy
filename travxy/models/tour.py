import sqlite3

class TourModel:
    def __init__(self, name, location, about):
        self.name = name
        self.location = location
        self.about = about

    def json(self):
        return{'name': self.name, 'location': self.location, 'about': self.about}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tours WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()

        query = "INSERT INTO tours VALUES (?, ?, ?)"
        cursor.execute(query, (self.name, self.location, self.about))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('trav_data.db')
        cursor = connection.cursor()
        query = "UPDATE tours SET location=?, about=? WHERE name=?"
        cursor.execute(query, (self.location, self.about, self.name))
        connection.commit()
        connection.close()
