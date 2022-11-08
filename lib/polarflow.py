import requests


def get(endpoint, access_token):
    kwargs = {}
    url = f"https://www.polaraccesslink.com/v3{endpoint}"
    print(url)
    kwargs["url"] = url
    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    kwargs["headers"] = headers

    response = requests.request('get', **kwargs)
    return parse_response(response)


def parse_response(response):
    if response.status_code >= 400:
      message = f"{response.status_code} {response.reason}: {response.text}"
      raise requests.HTTPError(message, response=response)

    if response.status_code == 204:
      return {}

    try:
      return response.json()
    except ValueError:
      return response.text
