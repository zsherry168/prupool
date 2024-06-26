from flask import render_template, request, redirect, url_for, flash, session
from app import app
from firebase_admin import auth
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import google.auth.transport.requests
import google.oauth2.id_token
import os
import requests

GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/google_signin')
def google_signin():
    return redirect(f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={url_for('google_callback', _external=True)}&scope=openid%20email%20profile&response_type=code")

@app.route('/google_callback')
def google_callback():
    code = request.args.get('code')
    if not code:
        flash('Authorization code not found', 'danger')
        return redirect(url_for('signup'))
    
    try:
        # Exchange the authorization code for an access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': url_for('google_callback', _external=True),
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=token_data)
        token_response_json = token_response.json()
        id_token_str = token_response_json.get('id_token')

        if not id_token_str:
            flash('Failed to obtain ID token', 'danger')
            return redirect(url_for('signup'))

        # Verify the ID token
        token_request = google.auth.transport.requests.Request()
        id_info = id_token.verify_oauth2_token(id_token_str, token_request, GOOGLE_CLIENT_ID)
        userid = id_info['sub']
        
        # Check if user exists in Firebase
        try:
            user = auth.get_user(userid)
        except auth.UserNotFoundError:
            # Create a new user in Firebase
            user = auth.create_user(
                uid=userid,
                email=id_info.get('email'),
                display_name=id_info.get('name')
            )
        
        session['user'] = {
            'name': user.display_name,
            'email': user.email,
            'uid': user.uid
        }
        flash('Signed in successfully!', 'success')
        return redirect(url_for('account'))
    except ValueError as e:
        flash(f'Invalid token: {e}', 'danger')
        return redirect(url_for('signup'))
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('signup'))

@app.route('/account')
def account():
    if 'user' not in session:
        flash('You need to sign in first', 'danger')
        return redirect(url_for('signup'))
    user = session['user']
    return render_template('account.html', user=user)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))