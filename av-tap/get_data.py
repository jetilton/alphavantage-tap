import json
from urllib import parse
import requests
import logging

import pandas as pd

from .utils import log_decorator

LOGGER = logging.getLogger(__name__)
LD = log_decorator(LOGGER)
FORMAT = "%(levelname)s - %(asctime)s - %(name)s - %(message)s"


@LD
def build_url(base_url, args_dict, path=None):
    # ref: https://stackoverflow.com/a/44552191
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(parse.urlparse(base_url))
    if path:
        url_parts[2] = path
    url_parts[4] = parse.urlencode(args_dict)
    return parse.urlunparse(url_parts)


@LD
def query_data(url):
    try:
        response = requests.get(url)
        LOGGER.info("Received {r.status_code} status code.")
    except:
        LOGGER.error(f"Error requesting {url}")
    return response


@LD
def response_to_json(response):
    if response.status_code != 200:
        LOGGER.warning("Status code is {response.status_code} not 200.")
        raise ValueError
    try:
        return json.loads(response.text)
    except:
        LOGGER.error("Error retrieving response.text")
        raise KeyError


@LD
def parse_json(json_data, data_type="Time Series (Daily)"):
    ts_data = json_data.get(data_type)
    result = []
    if not ts_data:
        LOGGER.warning(f"{data_type} not within data")
        raise KeyError
    meta_data = json_data.get("Meta Data")
    if not meta_data:
        LOGGER.warning("Meta Data not within data")
        raise KeyError
    symbol = meta_data["2. Symbol"]
    for date, value in ts_data.items():
        r = {"date_time": date, "symbol": symbol}
        for k, v in value.items():
            item = k.split(". ")[-1].replace(" ", "_")
            if item != "volume":
                val = float(v)
            else:
                val = int(v)
            r.update({item: val})
        result.append(r)
    return result


@LD
def get_data(base_url, config, api_key):
    result = []

    for symbol in config["symbols"]:
        args_dict = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "apikey": APIKEY,
        }
        url = build_url(base_url, args_dict, path="query")
        response = query_data(url)
        json_data = response_to_json(response)
        result += json_data
    return result