import os
import pickle
from dotenv import load_dotenv
from supabase import Client

load_dotenv()

TOKEN_PATH = os.getenv('TOKEN_PATH')

def existsSession(client:Client):
    if(os.path.exists(TOKEN_PATH)):
        with open(TOKEN_PATH , "rb") as file:
            data = pickle.load(file)
            response = client.auth.set_session(data.get("access_token") , data.get("refresh_token"))
            saveSession(response)
        return True
    else:
        return False
    
def saveSession(response):
    data = { 'access_token' : response.session.access_token , 'refresh_token' : response.session.refresh_token }
    with open(TOKEN_PATH , "wb") as file:
        pickle.dump(data, file)