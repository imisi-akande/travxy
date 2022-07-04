import psycopg2.extras
import logging
import configparser
from data_helper.users import user_tuple
from data_helper.categories import category_tuple
from data_helper.tours import tour_tuple

config = configparser.ConfigParser()
config.read('./data_helper/database.ini')

DB_Host = config['DEFAULT']['DB_HOST']
DB_Name = config['DEFAULT']['DATABASE_NAME']
DB_User = config['DEFAULT']['DATABASE_USERNAME']
DB_Password = config['DEFAULT']['DATABASE_PASSWORD']

try:
    connection = psycopg2.connect(host=DB_Host,
                                database=DB_Name,
                                user=DB_User,
                                password=DB_Password)
except psycopg2.DatabaseError as e:
        logging.warning("Unable to connect. Please Check database connection")
        raise e

user_cursor = connection.cursor()
insert_user_query = 'insert into users (email, username, password) values %s' 
psycopg2.extras.execute_values(
    user_cursor, insert_user_query, user_tuple, template=None, page_size=100
)
select_user_query = "SELECT * FROM users"
user_cursor.execute(select_user_query)
for row in user_cursor.fetchall():
    print(row)

category_cursor = connection.cursor()
insert_category_query = 'insert into categories (name) values %s'
psycopg2.extras.execute_values(
    category_cursor, insert_category_query, category_tuple, template=None, page_size=100
)
select_category_query = "SELECT * FROM categories"
category_cursor.execute(select_category_query)
for row in category_cursor.fetchall():
    print(row)

tour_cursor =  connection.cursor()
insert_tour_query = 'insert into tours (name, location, about, category_id) values %s'
psycopg2.extras.execute_values(tour_cursor, insert_tour_query, tour_tuple, template=None, page_size=100
)
select_tour_query = "SELECT * FROM tours"
tour_cursor.execute(select_tour_query)
for row in tour_cursor.fetchall():
    print(row)

connection.commit()
connection.close()