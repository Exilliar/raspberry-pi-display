import datetime
import json
import http.client
from dotenv import dotenv_values
import utils

dataJson = utils.readData()
config = dataJson["config"]["diary"]

env = dotenv_values("../.env")

conn = http.client.HTTPSConnection(env["DIARY_AUTH_DOMAIN"])

payload = f"{{\"client_id\":\"{env['DIARY_CLIENT_ID']}\",\"client_secret\":\"{env['DIARY_CLIENT_SECRET']}\",\"audience\":\"{env['DIARY_AUDIENCE']}\",\"grant_type\":\"client_credentials\"}}"

headers = { 'content-type': 'application/json' }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()
token = json.loads(data.decode("utf-8"))["access_token"]

dirConn = http.client.HTTPSConnection(env["DIARY_DOMAIN"])

currTime = datetime.datetime.now().strftime(config["datetimeFormat"])

headers = { 'authorization': f"Bearer {token}" }

endpoint = f"/api/entry/title?time={currTime}".replace(" ", "%20")

dirConn.request("GET", endpoint, headers=headers)

dirRes = dirConn.getresponse()
data = dirRes.read()

dataJson["displayed"] = False
dataJson["output"]["diary"]["title"] = data.decode("utf-8")
utils.writeData(dataJson)
