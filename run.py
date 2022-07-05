import os
from dotenv import load_dotenv

from travxy.app import create_app
load_dotenv('.env')

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
if __name__ == '__main__':
    app.run(port=5000, debug=True)