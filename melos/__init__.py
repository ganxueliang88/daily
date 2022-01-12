import json
import time

import requests
from twocaptcha import TwoCaptcha

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
solver = None


def get_recaptcha(api_key: str) -> str:
    global solver
    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey='6LdPsIUcAAAAAOjlufKN6Cpkqan8jWe2wPgnzxzY',
            url='https://www.melos.studio/login',
            version='v3',
            action='login',
            score=0.2,
            # invisible=1
        )

    except Exception as e:
        print("error: ", e)
        exit(-1)

    else:
        print('solved: ' + str(result))
        return result


def get_login(username, password, recaptcha) -> str:
    url = "https://app.melos.studio/graphql"
    payload = {
        "operationName": "loginByEmail",
        "variables": {
            "email": username,
            "password": password,
            "recaptcha": recaptcha["code"],
        },
        "query": "query loginByEmail($email: String!, $password: String!, $recaptcha: String){\n  loginByEmail(email: $email, password: $password, recaptcha: $recaptcha) {\n    pwl\n    acc\n    userId\n    nonce\n    expires\n    isFirstLogin\n    pub\n    sign\n    isFirstLogin\n    __typename\n  }\n}\n "
    }
    headers = {
        'authority': 'app.melos.studio',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': '*/*',
        'content-type': 'application/json',
        'authorization': '',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.melos.studio',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.melos.studio/',
        'accept-language': 'en-US,en;q=0.9'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    #print(response.text)
    if (response.status_code != 200):
        print("login err")
        exit(-1)
    data = json.loads(response.text)
    if ("errors" in data.keys()):
        print("login err")
        if ("Recaptcha error" in data):
            solver.report(recaptcha["captchaId"], False)
        exit(-1)
    solver.report(recaptcha["captchaId"], True)
    return data["data"]["loginByEmail"]["acc"]


def wave(acc: str):
    url = "https://app.melos.studio/graphql"
    payload = {
        "operationName": "collectWaves",
        "variables": {
            "catagory": "Activity"
        },
        "query": "mutation collectWaves($catagory: String) { collectWaves(catagory: $catagory)}"
    }
    headers = {
        'authority': 'app.melos.studio',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': '*/*',
        'content-type': 'application/json',
        'authorization': 'Bearer ' + acc,
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.melos.studio',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.melos.studio/',
        'accept-language': 'en-US,en;q=0.9'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.text)


def do_daily(config_file: str):
    with open(config_file) as config_file:
        config = json.load(config_file)
        api_key = config["2captcha_apikey"]
        if "melos" not in config.keys():
            return
        for user in config['melos']:
            recaptcha = get_recaptcha(api_key)
            time.sleep(1)
            username = user["username"]
            password = user["password"]
            acc = get_login(username, password, recaptcha)
            wave(acc)


if __name__ == "__main__":
    do_daily("../config/config_self.json")
