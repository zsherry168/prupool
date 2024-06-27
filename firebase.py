import firebase_admin
from firebase_admin import credentials
import os
import json

# Load credentials from the file
with open(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as f:
    cred_dict = json.load(f)

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

def save_trip_to_firebase(trip):
    db = firebase_admin.firestore.client()
    db.collection('trips').add(trip)

def book_trip(trip):
    db = firebase_admin.firestore.client()
    for user in trip['carpool']:
        user_ref = db.collection('users').document(user)
        user_ref.update({
            'trips': firebase_admin.firestore.ArrayUnion([trip])
        })
