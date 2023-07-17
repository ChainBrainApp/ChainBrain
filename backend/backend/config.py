"""Default configuration

Use env var to override
"""
import os
from dotenv import load_dotenv


load_dotenv()

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
THEGRAPH_API_KEY = os.getenv("THEGRAPH_API_KEY")
BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")
