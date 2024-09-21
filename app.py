import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.')
CORS(app)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/auth/google', methods=['POST'])
def google_auth():
    token = request.json['token']
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']

        return jsonify({
            'status': 'success',
            'user': {
                'id': userid,
                'email': email,
                'name': name
            }
        }), 200

    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 400

@app.route('/get-google-client-id')
def get_google_client_id():
    return jsonify({
        'clientId': GOOGLE_CLIENT_ID
    })

if __name__ == '__main__':
    app.run(debug=True)
