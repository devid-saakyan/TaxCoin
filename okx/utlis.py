import base64
import datetime as dt
import hmac
import requests
import hashlib

def okx_ref(uid):
    BASE_URL = 'https://okx.com'
    APIKEY = '5c5be7af-88ef-4230-ba63-2cc46f28cd68'
    APISECRET = '356A8B6A3AC17DACC0FC6EB1A6EA72DE'
    PASS = "David2024!"

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
    data = requests.get(BASE_URL + request_path, headers=headers).json()
    if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
        vol_month = float(data["data"][0].get("volMonth", 0))
        return True, vol_month
    return False, 0


def CheckKyc(OkxId):
    try:
        if len(okx_ref(OkxId)['data'][0].get('kycTime')) > 1:
            return True
        else:
            return False
    except:
        return False


def check_okx_keys(api_key, api_secret):
    BASE_URL = 'https://okx.com'
    APIKEY = api_key
    APISECRET = api_secret
    PASS = "David20240!"

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

    request_path = "/api/v5/account/balance"
    headers = get_header("GET", request_path)
    response = requests.get(BASE_URL + request_path, headers=headers)
    if str(response.json()) == "{'msg': 'Request header OK-ACCESS-PASSPHRASE incorrect.', 'code': '50105'}":
        return True
    else:
        return False


if __name__ == '__main__':
    print(okx_ref(537722074245431945))
    print(okx_ref(582748711890208025))
    #print(check_okx_keys('5c5be7af-88ef-4230-ba63-2cc46f28cd68','356A8B6A3AC17DACC0FC6EB1A6EA72DE'))