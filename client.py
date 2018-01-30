#!/usr/bin/env python
import json
import requests
import datetime
import hashlib
import hmac

# Deze drie variabelen aanpassen naar je eigen shop
API_Key = "< API public key >"
API_Secret = "< API secret >"
API_Host = "https://demo.ccvshop.nl"

API_Prefix = "/api/rest/v1"


def get_headers(method, uri, data):
    upper_method = str.upper(method)
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    hash_string = API_Key + "|" + upper_method + "|" + uri + "|" + data + "|" + timestamp
    hash_hex = hmac.new(API_Secret.encode("ascii"), hash_string.encode("ascii"), hashlib.sha512).hexdigest()
    headers = {
        "x-date": timestamp,
        "x-hash": hash_hex,
        "x-public": API_Key
    }
    return headers


# voorbeeld van een HTTPS GET request
def ccv_shop_get(path, data):
    uri = API_Prefix + path
    url = API_Host + uri
    headers = get_headers("GET", uri, data)
    res = requests.get(url, data=data, headers=headers)
    return res


res = ccv_shop_get("/orders", "")
print(res.status_code)
if res.status_code == 200:
    orders = json.loads(res.text)
    print(orders)
