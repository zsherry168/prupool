import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK with a service account key
cred = credentials.Certificate('./credentials.json')
firebase_admin.initialize_app(cred)
