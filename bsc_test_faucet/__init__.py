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
            sitekey='6LeEQewUAAAAAFo1d0OMORFXn3YaB38BZGdZiLYR',
            url='https://testnet.binance.org/faucet-smart',
            invisible=1
        )

    except Exception as e:
        print("error: ", e)
        exit(-1)

    else:
        print('solved: ' + str(result))
        return result


def faucet(address, coin, captcha):
    ws = create_connection("wss://testnet.binance.org/faucet-smart/api")
    request = {
        "url": address,
        "symbol": coin,  # 1 BNB， 0.1 BTC， 10 BUSD， 10 DAI，0.1 ETH， 10 USDC， 10 USDT， 10 XRP
        "tier": 0,
        "captcha": captcha['code']
    }

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
    ws.close()


def do_daily(config):
    if "bsc_test" not in config.keys():
        return
    api_key = config["2captcha_apikey"]
    address = config["bsc_test"]["eth"]
    coin = config["bsc_test"]["coin"]
    recaptcha = get_recaptcha(api_key)
    faucet(address, coin, recaptcha)


if __name__ == "__main__":
    with open("../config/config_self.json") as config_file:
        config = json.load(config_file)
        do_daily(config)
