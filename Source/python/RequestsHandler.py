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
    "standings" : lambda date: _requestHandler(f"https://api-web.nhle.com/v1/standings/{date}"),
}

def getData(arguments) -> dict:
    """
    Fetches the given NHL data from the api

    arguments : argparse.Namespace
        Given user arguements

    return dict | str
        JSON response of the requested data
    """

    DataKey : str = arguments.data
    Date : str = arguments.date

    return RequestMappings[DataKey](Date)