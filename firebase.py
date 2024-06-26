import firebase_admin
from firebase_admin import credentials
import os
import json

# Load credentials from environment variable
cred_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
