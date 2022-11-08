from . import user
from . import polarflow
import requests
from flask import Flask, request, redirect

CALLBACK_PORT = 5000
CALLBACK_ENDPOINT = "/oauth2_callback"

app = Flask(__name__)
user_secret = user.get_user_secrets()

def get_access_token(authorization_code):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json;charset=UTF-8"
    }

    data = {
        "grant_type": "authorization_code",
        "code": authorization_code
    }

    kwargs = {}
    kwargs["headers"] = headers
    kwargs["url"] = "https://polarremote.com/v2/oauth2/token"
    kwargs["data"] = data
    kwargs["auth"] = requests.auth.HTTPBasicAuth(user_secret["client_id"], user_secret["client_secret"])

    response = requests.request('post', **kwargs)
    return polarflow.parse_response(response)

def shutdown():
  shutdown_func = request.environ.get('werkzeug.server.shutdown')
  if shutdown_func is not None:
    shutdown_func()

def register(access_token, member_id):
    kwargs = {}
    kwargs["url"] = "https://www.polaraccesslink.com/v3" + "/users"
    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    kwargs['headers'] = headers
    kwargs['json'] = {"member-id": member_id}

    response = requests.request('post', **kwargs)
    return polarflow.parse_response(response)

@app.route("/")
def authorize():
    return redirect(f"https://flow.polar.com/oauth2/authorization?response_type=code&client_id={user_secret['client_id']}")

@app.route(CALLBACK_ENDPOINT)
def callback():
    authorization_code = request.args.get("code")
    token_response = get_access_token(authorization_code)

    user_id = token_response["x_user_id"]
    access_token = token_response["access_token"]
    user.dump_access_token(user_id, access_token)

    try:
        register(access_token, user_id)
    except requests.exceptions.HTTPError as err:
        # Error 409 Conflict means that the user has already been registered for this client.
        # That error can be ignored in this example.
        if err.response.status_code != 409:
            raise err

    shutdown()
    return "Client authorized! You can now close this page."

def run():
  print(f"Navigate to http://localhost:{CALLBACK_PORT}/ for authorization.\n")
  app.run(host='localhost', port=CALLBACK_PORT)
