from flask import Flask, redirect, request
from google.oauth2.credentials import Credentials
from google.oauth2.credentials import client

app = Flask(__name__)

@app.route('/connect')
def connect():
    flow = client.OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=['https://www.googleapis.com/auth/drive'], redirect_uri='http://localhost:5000/callback')
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    flow = client.OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=['https://www.googleapis.com/auth/drive'], redirect_uri='http://localhost:5000/callback')
    auth_response = request.url
    creds = flow.fetch_token(authorization_response=auth_response)
    creds = Credentials.from_authorized_user_info(info=creds.to_json(), client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # Save the credentials in a session or a database for future use
    return 'Connected to Google Drive'

if __name__ == '__main__':
    app.run(debug=True)
