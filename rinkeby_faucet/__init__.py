import json
import time

import requests
from websocket import create_connection
from twocaptcha import TwoCaptcha

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
solver = None


def get_recaptcha(api_key: str) -> dict:
    global solver
    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey='6LeaRh0UAAAAAD5G5UXcFnftTNfnZ7Dk2eGNWWdb',
            url='https://www.rinkeby.io/#faucet',
            invisible=1
        )

    except Exception as e:
        print("error: ", e)
        exit(-1)

    else:
        print('solved: ' + str(result))
        return result


def faucet(url, tier, captcha):
    request = {
        "url": url,
        "tier": tier,  # 0:3eth/8h, 1:7.5eth/day,2:18.75/3day
        "captcha": captcha['code']
    }

    ws = create_connection("wss://faucet.rinkeby.io/api")
    try:
        print("Sending...")
        ws.send(json.dumps(request))
        print("Receiving...")
        for i in range(20):
            result = ws.recv()
            print(result)
            result = json.loads(result)
            if "error" in result.keys():
                print(result["error"])
                if "you're a robot" in result["error"]:
                    solver.report(captcha["captchaId"], False)
                else:
                    solver.report(captcha["captchaId"], True)
                break
            elif "success" in result.keys():
                solver.report(captcha["captchaId"], True)
                break
    except Exception as e:
        print(e)
    ws.close()


def do_daily(config):
    print("rinkeby test faucet:")
    if "rinkeby" not in config.keys():
        return
    api_key = config["2captcha_apikey"]
    url = config["rinkeby"]["url"]
    tier = int(config["rinkeby"]["tier"])
    recaptcha = get_recaptcha(api_key)
    faucet(url, tier, recaptcha)


if __name__ == "__main__":
    with open("../config/config_self.json") as config_file:
        config = json.load(config_file)
        do_daily(config)
