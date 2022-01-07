import requests

def wave():
    url = "https://app.melos.studio/graphql"
    payload='''{
        "operationName": "collectWaves",
        "variables": {
                "catagory": "Activity"    
                },    
        "query": "mutation collectWaves($catagory: String) { collectWaves(catagory: $catagory)}"
        }'''
    headers = {
      'authority': 'app.melos.studio',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
      'accept': '*/*',
      'content-type': 'application/json',
      'authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2MWQ1ZjAxMmM2Mjk1NDQ0ZjBlM2EwYmYiLCJpYXQiOjE2NDE1NDI0ODd9.xTdbuelxlF5XWNuV_YrMmGDS8a1_nR9dnyT6lIuwdH86AIg86fTpQjOBVJDev_YJUQbxdpZPCFrO-J4jH9mf1A',
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

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__=="__main__":
    wave()