from flask import render_template, request, redirect, url_for, flash, session
from app import app
from firebase_admin import auth
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import google.auth.transport.requests
import google.oauth2.id_token
import os
import requests
import json
from distance_calculator import calculate_distance

GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']

test_users = []

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')
  
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
        token_request = Request()
        id_info = id_token.verify_oauth2_token(id_token_str, token_request, GOOGLE_CLIENT_ID)
        userid = id_info['sub']
        
        # Check if user exists in Firebase
        try:
            user = auth.get_user(userid)
        except auth.UserNotFoundError:
            # Create a new user in Firebase with default preferences and points
            user = auth.create_user(
                uid=userid,
                email=id_info.get('email'),
                display_name=id_info.get('name')
            )
            # Set default preferences and points
            auth.set_custom_user_claims(user.uid, {
                'preferences': {
                    'age': None,
                    'role': None,
                    'gender': None,
                    'days_going_to_work': [],
                    'driving_to': None,
                    'type_of_car': None,
                    'seats_in_car': None,
                    'work_building': None,
                    'home_address': None
                },
                'points': 0  # Initialize points to 0
            })
        
        session['user'] = {
            'name': user.display_name,
            'email': user.email,
            'uid': user.uid,
            'picture': id_info.get('picture'),  # Add profile picture
            'points': user.custom_claims.get('points', 0)  # Add points to session
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
    
    user_id = session['user']['uid']
    user = auth.get_user(user_id)
    preferences = user.custom_claims.get('preferences', {}) or {}
    points = user.custom_claims.get('points', 0)  # Ensure points are retrieved
    
    return render_template('account.html', user=session['user'], preferences=preferences, points=points)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    if 'user' not in session:
        flash('You need to sign in first', 'danger')
        return redirect(url_for('signup'))
    
    user_id = session['user']['uid']
    days_going_to_work = request.form.get('days_going_to_work', '').split(', ')
    
    preferences = {
        'age': request.form.get('age'),
        'role': request.form.get('role'),
        'gender': request.form.get('gender'),
        'days_going_to_work': days_going_to_work,
        'driving_to': request.form.get('driving_to'),
        'type_of_car': request.form.get('type_of_car'),
        'seats_in_car': request.form.get('seats_in_car'),
        'work_building': request.form.get('work_building'),
        'home_address': request.form.get('home_address')
    }
    
    try:
        # Update user preferences in Firebase
        auth.set_custom_user_claims(user_id, {'preferences': preferences})
        flash('Preferences updated successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/distance')
def distance():
    if 'user' not in session:
        flash('You need to sign in first', 'danger')
        return redirect(url_for('signup'))

    user_id = session['user']['uid']
    user = auth.get_user(user_id)
    preferences = user.custom_claims.get('preferences', {})
    
    return render_template('distance.html', preferences=preferences)

@app.route('/calculate_distance', methods=['POST'])
def calculate_distance_route():
    if 'user' not in session:
        flash('You need to sign in first', 'danger')
        return redirect(url_for('signup'))

    home_address = request.form.get('home_address')
    work_building = request.form.get('work_building')

    # Map work building to its address
    work_building_addresses = {
        'tower': 'Prudential Tower, Newark, NJ',
        'wash': 'Prudential Insurance Company of America - Washington Building, Newark, NJ',
        'plaza': 'Prudential Headquarters - Plaza Building, Newark, NJ'
    }

    work_building_address = work_building_addresses.get(work_building)

    if not home_address or not work_building_address:
        flash('Invalid addresses provided', 'danger')
        return redirect(url_for('distance'))

    try:
        distance, duration = calculate_distance(home_address, work_building_address)
        return render_template('distance.html', distance=distance, duration=duration, preferences={'home_address': home_address, 'work_building': work_building})
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('distance'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('You need to sign in first', 'danger')
        return redirect(url_for('signup'))
    
    user_id = session['user']['uid']
    user = auth.get_user(user_id)
    preferences = user.custom_claims.get('preferences', {})
    points = user.custom_claims.get('points', 0)  # Ensure points are retrieved
    
    return render_template('profile.html', user=session['user'], preferences=preferences, points=points)

@app.route('/other-profile')
def other_profile():
    return render_template('other-profile.html')

@app.route('/test-users', methods=['GET', 'POST'])
def test_users_page():
    if request.method == 'POST':
        new_user = {
            'name': request.form['name'],
            'email': request.form['email'],
            'home_address': request.form['home_address'],
            'work_building': request.form['work_building'],
            'type_of_car': request.form['type_of_car'],
            'seats_in_car': request.form['seats_in_car'],
            'points': request.form['points']
        }
        
        # Create a new user in Firebase
        try:
            user = auth.create_user(
                email=new_user['email'],
                display_name=new_user['name']
            )
            # Set custom claims for the user
            auth.set_custom_user_claims(user.uid, {
                'preferences': {
                    'home_address': new_user['home_address'],
                    'work_building': new_user['work_building'],
                    'type_of_car': new_user['type_of_car'],
                    'seats_in_car': new_user['seats_in_car']
                },
                'points': new_user['points']
            })
            flash('Test user created successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        
        return redirect(url_for('test_users_page'))
    
    # Fetch all users with custom claims
    test_users = []
    for user in auth.list_users().iterate_all():
        if user.custom_claims:
            test_users.append({
                'name': user.display_name,
                'email': user.email,
                'home_address': user.custom_claims.get('preferences', {}).get('home_address', 'N/A'),
                'work_building': user.custom_claims.get('preferences', {}).get('work_building', 'N/A'),
                'type_of_car': user.custom_claims.get('preferences', {}).get('type_of_car', 'N/A'),
                'seats_in_car': user.custom_claims.get('preferences', {}).get('seats_in_car', 'N/A'),
                'points': user.custom_claims.get('points', 'N/A')
            })
    
    return render_template('test_users.html', test_users=test_users)
