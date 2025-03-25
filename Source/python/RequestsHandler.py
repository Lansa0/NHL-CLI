import requests

def _requestHandler(url : str) -> dict:
    """
    Handles fetching the HTTP requests from the NHL api

    url : str
        The URL to the appropriate endpoint

    return dict
        Requested JSON response from the api
    """

    Response = requests.get(url, timeout = 3)
    Response.raise_for_status()

    return Response.json()

RequestMappings : dict[str, callable] = {
    "standings" : lambda args: _requestHandler(f"https://api-web.nhle.com/v1/standings/{args.date}"),
    "scores" : lambda args: _requestHandler(f"https://api-web.nhle.com/v1/score/{args.date}")
}

def getData(arguments) -> dict:
    """
    Fetches the given NHL data from the api

    arguments : argparse.Namespace
        Given user arguements

    return dict | str
        JSON response of the requested data
    """

    return RequestMappings[arguments.data](arguments)