from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/other-profile')
def other_profile():
    return render_template('other-profile.html')