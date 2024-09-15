import time
import hmac
import requests
import hashlib
import json


def bybit_ref(uid):
    APIKEY = 't7LDTWIOGj8OJFdPWb'
    APISECRET = 'XkBXKdLEcE0XePJriPKsIVP2VKjBA61ip0Pa'

    payload = 'uid=' + uid
    recv_window = str(5000)
    timestamp = str(int(time.time() * 1000))
    param_str = timestamp + APIKEY + recv_window + payload
    hash = hmac.new(bytes(APISECRET, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()

    headers = {
        'X-BAPI-API-KEY': APIKEY,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }

    url = "https://api.bybit.com/v5/user/aff-customer-info?"
    response = requests.get(url + payload, headers=headers)
    print(response.json())
    try:
        if len(response.json().get('result')) > 0:
            return True, response.json()#.get('result').get('takerVol30Day')
        else:
            return False, 0
    except:
        return response.json()


if __name__ == '__main__':
    print(bybit_ref('266167900'))
    print(bybit_ref('2661679000'))