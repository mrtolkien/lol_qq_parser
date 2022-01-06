import requests
from requests.models import HTTPError

from lol_qq_parser.utils import Config


def query_tjstats(endpoint: str):
    query_url = f"{Config.root_url}{endpoint}"

    response = requests.get(query_url, headers=Config.headers)

    # Raising if we do not get a 200 code to makes sure we don't crash on .json()
    response.raise_for_status()

    # The QQ API actually does net always raise HTTP Errors but passes it in the body...
    data = response.json()

    try:
        assert data["success"]
    except AssertionError:
        raise HTTPError(data["errMsg"])

    return data
