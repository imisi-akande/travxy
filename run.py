import os
from dotenv import load_dotenv

from travxy import create_app
from travxy.config import DevelopmentConfig

app = create_app()
if __name__ == '__main__':
    app.run(port=5000, debug=True)