import os
import secrets
from google.cloud import secretmanager
from dotenv import load_dotenv
load_dotenv()


#client = secretmanager.SecretManagerServiceClient()
#client.access_secret_version('SC_CLIENT_ID')
#payload = response.payload.data.decode('UTF-8')
# print('Plaintext: {}'.format(payload))


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
ADMIN_ID = os.getenv('ADMIN_ID')
