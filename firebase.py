import firebase_admin
from firebase_admin import credentials
import os
import json

# Load credentials from the file
with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as f:
    cred_dict = json.load(f)

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
