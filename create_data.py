import logging
import configparser
import os

from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read('./data_helper/database.ini')

DB_Host = config['DEFAULT']['DB_HOST']
DB_Name = config['DEFAULT']['DATABASE_NAME']
DB_User = config['DEFAULT']['DATABASE_USERNAME']
DB_Password = config['DEFAULT']['DATABASE_PASSWORD']

engine = create_engine(f"postgresql://{DB_User}:{DB_Password}@{DB_Host}/{DB_Name}")
try:
    with engine.connect() as conn:
        base_path = "./data_helper/"
        paths = ["users.sql", "roles.sql", "tourists.sql", "categories.sql",
                "tours.sql", "tour_category.sql", "details.sql",
                "tourist_detail.sql", "tourist_experience.sql"]
        for path in paths:
            full_path = os.path.join(base_path, path)
            file = open(full_path)
            statement = file.read()
            conn.execute(statement)
except Exception as e:
    logging.warning("Unable to connect. Please Check database connection")
    raise e