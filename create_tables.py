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
tour_table = "CREATE TABLE IF NOT EXISTS tours(name text PRIMARY KEY, location text, about text)"
cursor.execute(tour_table)
tours = [
    ("Shark Bay", "Australia", "Beautiful sharks everywhere"),
    ("Paracas", "Peru", "Funfilled place"),
    ("Algarve", "Portugal", "Sunny microclimate and affordable places to stay"),
    ("Paris", "France", "This city that never sleeps"),
    ("Death Valley", "California", "Vast area of extremes: with snowy peaks, scorching sands")
] 
tours_query = "INSERT INTO tours VALUES(?,?,?)"
cursor.executemany(tours_query, tours)
select_user_query = "SELECT * FROM users"
for row in cursor.execute(select_user_query):
    print(row)

select_tour_query = "SELECT * FROM tours"
for row in cursor.execute(select_tour_query):
    print(row)

connection.commit()
connection.close()



