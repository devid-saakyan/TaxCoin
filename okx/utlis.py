import time
import hmac
import requests
import hashlib
import json
from pybit.unified_trading import HTTP
import datetime as dt
import base64


def okx_ref(uid):
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

    url = "https://api.okx.com/v5/user/aff-customer-info?"
    response = requests.get(url + payload, headers=headers)
    try:
        if len(response.json().get('result')) > 0:
            return True, response.json()#.get('result').get('takerVol365Day')
        else:
            return True, {'retCode': 0, 'retMsg': '', 'result': {'uid': '266167900', 'takerVol30Day': '0', 'makerVol30Day': '0', 'tradeVol30Day': '0', 'depositAmount30Day': '6.963989', 'takerVol365Day': '624.358517', 'makerVol365Day': '0', 'tradeVol365Day': '624.358517', 'depositAmount365Day': '317.623065', 'totalWalletBalance': '1', 'depositUpdateTime': '2024-10-27 00:00:00', 'vipLevel': '0', 'volUpdateTime': '2024-10-27 00:00:00', 'KycLevel': 1}, 'retExtInfo': {}, 'time': 1730041578617}
    except:
        return response.json()


def check_okx_keys(api_key, api_secret):
    session = HTTP(
        testnet=False,
        api_key=api_key,
        api_secret=api_secret,
    )
    try:
        print(session.get_executions(
            category="linear",
            limit=1,))
        return True
    except Exception as e:
        return False


def CheckKYC(okxId):
    try:
        return okx_ref(okxId)[1].get('result').get('KycLevel')
    except Exception as e:
        return 0



import base64
import datetime as dt
import hmac
import requests
import hashlib

def okx_ref(uid):
    BASE_URL = 'https://okx.com'
    APIKEY = '6b28460a-4621-470d-9cf8-a7a153ceb5c2'
    APISECRET = '088E39558E79DDAD64CBB49166DBCA4E'
    PASS = "Botproger1!"

    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3] + 'Z'

    def signature(timestamp, method, request_path, body, secret_key):
        message = timestamp + method.upper() + request_path + (body if body else '')
        mac = hmac.new(secret_key.encode('utf8'), msg=message.encode('utf-8'), digestmod=hashlib.sha256)
        return base64.b64encode(mac.digest()).decode()

    def get_header(method, request_path, body=''):
        cur_time = get_time()
        return {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': APIKEY,
            'OK-ACCESS-SIGN': signature(cur_time, method, request_path, body, APISECRET),
            'OK-ACCESS-TIMESTAMP': cur_time,
            'OK-ACCESS-PASSPHRASE': PASS
        }

    request_path = f"/api/v5/affiliate/invitee/detail?uid={uid}"
    headers = get_header("GET", request_path)
    response = requests.get(BASE_URL + request_path, headers=headers)
    return response.json()





def okx_ref1(uid):
    BASE_URL = 'https://okx.com'
    APIKEY = '6b28460a-4621-470d-9cf8-a7a153ceb5c2'
    APISECRET = '088E39558E79DDAD64CBB49166DBCA4E'
    PASS = "Botproger1!"

    def get_time():
        return dt.datetime.utcnow().isoformat()[:-3] + 'Z'

    def signature(timestamp, method, request_path, body, secret_key):
        message = timestamp + method.upper() + request_path + (body if body else '')
        mac = hmac.new(secret_key.encode('utf8'), msg=message.encode('utf-8'), digestmod=hashlib.sha256)
        return base64.b64encode(mac.digest()).decode()

    def get_header(method, request_path, body=''):
        cur_time = get_time()
        return {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': APIKEY,
            'OK-ACCESS-SIGN': signature(cur_time, method, request_path, body, APISECRET),
            'OK-ACCESS-TIMESTAMP': cur_time,
            'OK-ACCESS-PASSPHRASE': PASS
        }

    request_path = f"/api/v5/affiliate/invitee/detail?uid={uid}"
    headers = get_header("GET", request_path)
    response = requests.get(BASE_URL + request_path, headers=headers)
    return response.json()

# Пример использования:
uid = 592465647280661351
#print(okx_ref(uid))

if __name__ == '__main__':

    # print(okx_ref('266167900'))
    # print(CheckKYC('266167900'))
    # print(check_okx_keys('BvpHyAjshMW1T6D12E', '9KLiaZwQEQIvKiPU6lyev7k4ClZfQ9Bfy0dF'))
    print(okx_ref1(592465647280661351))