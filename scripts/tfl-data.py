import http.client
import json
import utils

dataJson = utils.readData()

config = dataJson["config"]["tfl"]

conn = http.client.HTTPSConnection("api.tfl.gov.uk")

lines = config["lines"]

lineData = {}

for line in lines:
    lineData[line] = {
        "statuses": []
    }

statusEndpoint = f"/Line/{','.join(lines)}/Status"

conn.request("GET", statusEndpoint)

statusRes = conn.getresponse()
statuses = json.loads(statusRes.read())

for status in statuses:
    line = status["id"]
    for s in status["lineStatuses"]:
        lineData[line]["statuses"].append({
            "statusSeverity": s["statusSeverity"],
            "statusSeverityDescription": s["statusSeverityDescription"],
            "reason": s["reason"] if "reason" in s else None
        })

dataJson["displayed"] = False
dataJson["output"]["tfl"] = lineData
utils.writeData(dataJson)
