import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load variables from .env file

        # Define your variables here
        self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

config = Config()