import json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from flask import Flask, request, redirect


CALLBACK_PORT = 5000
CALLBACK_ENDPOINT = "/oauth2_callback"
userid_file = 'data/userid.json'

def getUserId():
    with open(userid_file, 'r') as file:
        return json.load(file)


def setUserId(userId):
    with open(userid_file, 'w') as file:
        return json.dump(userId, file, indent=True)


userId = getUserId()
app = Flask(__name__)


@app.route("/")
def authorize():
    return redirect(f'https://flow.polar.com/oauth2/authorization?response_type=code&client_id={userId.client_id}')


@app.route(CALLBACK_ENDPOINT)
def callback():
    authorization_code = request.args.get("code")
    token_response = get_access_token(authorization_code)

    userId['user_id'] = token_response["x_user_id"]
    userId['access_token'] = token_response["access_token"]
    setUserId(userId)

    #
    # Register the user as a user of the application.
    # This must be done before the user's data can be accessed through AccessLink.
    #
    try:
        register(userId['access_token'], userId['user_id'])
    except requests.exceptions.HTTPError as err:
        # Error 409 Conflict means that the user has already been registered for this client.
        # That error can be ignored in this example.
        if err.response.status_code != 409:
            raise err

    shutdown()
    return "Client authorized! You can now close this page."


def parse_response(response):
    if response.status_code >= 400:
        message = "{code} {reason}: {body}".format(code=response.status_code,
                                                   reason=response.reason,
                                                   body=response.text)
        raise HTTPError(message, response=response)

    if response.status_code == 204:
        return {}

    try:
        return response.json()
    except ValueError:
        return response.text


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
    return parse_response(response)


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
    kwargs["auth"] = HTTPBasicAuth(userId.client_id, userId.client_secret)

    response = requests.request('post', **kwargs)
    return parse_response(response)


def authenticate():
    print("Navigate to http://localhost:{port}/ for authorization.\n".format(port=CALLBACK_PORT))
    app.run(host='localhost', port=CALLBACK_PORT)


def get(endpoint, access_token):
    kwargs = {}
    kwargs["url"] = "https://www.polaraccesslink.com/v3" + endpoint
    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    kwargs["headers"] = headers

    response = requests.request('get', **kwargs)
    return parse_response(response)


if __name__ == '__main__':
    authenticate()
