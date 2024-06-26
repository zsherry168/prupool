from flask import Flask
import firebase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = os.getenv('SECRET_KEY')

from app import routes