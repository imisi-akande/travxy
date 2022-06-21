import sqlite3

connection = sqlite3.connect('trav_data.db')

cursor = connection.cursor()

user_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(user_table)

users = [
        (1, 'bob', 'asdf'),
        (2, 'siri', 'asdf'),
        (3, 'kate', 'asdf'),
        (4, 'james', 'asdf'),
        (5, 'esther', 'asdf')
        ]
users_query = "INSERT INTO users VALUES(?, ?, ?)"

cursor.executemany(users_query, users)
tour_table = "CREATE TABLE tours(id int, name text, location text, departure text, experience text, cost real, duration int)"
cursor.execute(tour_table)
tours = [
    (1, "Shark Bay", "Australia", "Cameroun", "The area is diverse", 100, 24),
    (2, "Paracas", "Peru", "Saudi Arabia", "I had fun", 200, 43),
    (3, "Algarve", "Portugal", "South Africa", "It has its own sunny microclimate and affordable places to stay", 400, 22),
    (4, "Paris", "France", "Netherland", "This city never sleeps", 500, 52),
    (5, "Death Valley", "California", "Ghana", "vast area of extremes: with snowy peaks, scorching sands", 500, 59)
]
tours_query = "INSERT INTO tours VALUES(?,?,?,?,?,?,?)"
cursor.executemany(tours_query, tours)
select_user_query = "SELECT * FROM users"
for row in cursor.execute(select_user_query):
    print(row)

select_tour_query = "SELECT * FROM tours"
for row in cursor.execute(select_tour_query):
    print(row)

connection.commit()
connection.close()



