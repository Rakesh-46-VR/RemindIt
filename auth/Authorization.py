import webbrowser
from flask import Flask, request, render_template
import threading
import os
from dotenv import load_dotenv
import pickle
from werkzeug.serving import make_server

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_PATH = os.getenv('TOKEN_PATH')

class AuthManager:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.app = Flask(__name__)
        self.server = None
        self.loggedin = False
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/callback', methods=['GET'])
        def callback():
            return render_template('index.html')

        @self.app.route('/receive_token', methods=['POST'])
        def receive_token():
            data = request.get_json()
            if data.get('access_token') and data.get('refresh_token'):
                self.access_token = data['access_token']
                self.refresh_token = data['refresh_token']
                data_to_save = {'access_token': self.access_token, 'refresh_token': self.refresh_token}
                with open(TOKEN_PATH, "wb") as file:
                    pickle.dump(data_to_save, file)
                    self.loggedin = True
                    
                # Respond to the client before shutting down the server
                response = {"message": "Token received successfully"}
                shutdown_thread = threading.Thread(target=self.stop_server)
                shutdown_thread.start()
                return response
            else:
                response = {"message": "Token not received"}
                return response, 400

    def start_server(self):
        self.server = make_server('127.0.0.1', 3000, self.app)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop_server(self):
        if self.server:
            self.server.shutdown()

    def start_oauth_flow(self):
        auth_url = f"{SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to={REDIRECT_URI}"
        webbrowser.open(auth_url)
        self.start_server()