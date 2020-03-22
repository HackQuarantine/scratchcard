import os
import secrets
from dotenv import load_dotenv
load_dotenv()

# Our configuration
NAME = os.getenv('NAME')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORIZE_URL = os.getenv('AUTHORIZE_URL')
ACCESS_TOKEN_URL = os.getenv('ACCESS_TOKEN_URL')
OAUTH_SCOPE = os.getenv('OAUTH_SCOPE')
BASE_URL = os.getenv('BASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_bytes(32)
DATABASE_URI = os.getenv('DATABASE_URI')
USER_INFO = os.getenv('USER_INFO')
