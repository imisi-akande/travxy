import psycopg2.extras
import logging
import configparser
config = configparser.ConfigParser()
config.read('database.ini')

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

cursor = connection.cursor()

user_tuple =[
    ('kike@gmail.com', 'kike','kike'),
    ('burna@gmail.com', 'burna','burna'),
    ('sunday@gmail.com', 'sunday','sunday')
]
insert_query = 'insert into users (email, username, password) values %s' 
psycopg2.extras.execute_values (
    cursor, insert_query, user_tuple, template=None, page_size=100
)

connection.commit()
connection.close()