import utils
import http.client
from dotenv import dotenv_values
import json

# time - the time
# screenTemperature - the temperature (excluding wind, sun, etc)
# feelsLikeTemperature - the "feels like" temperature
# probOfPrecipitation - probability of rain
# totalSnowAmount - amount of snow

env = dotenv_values("../.env")

dataJson = utils.readData()
config = dataJson["config"]["weather"]

selectedLocation = config["locations"][config["selectedLocation"]]

excludeParameterMetadata = True
includeLocationName = True
latitude = selectedLocation["latitude"]
longitude = selectedLocation["longitude"]
timeStep = config["availableTimesteps"][config["selectedTimestep"]]
apikey = env["GLOBAL_SPOT_KEY"]

conn = http.client.HTTPSConnection("data.hub.api.metoffice.gov.uk")

endpoint = f"/sitespecific/v0/point/{timeStep}?excludeParameterMetadata={excludeParameterMetadata}&includeLocationName={includeLocationName}&latitude={latitude}&longitude={longitude}"

headers = { "apikey": apikey }

conn.request("GET", endpoint, headers=headers)

res = conn.getresponse()
weatherData = json.loads(res.read())

properties = weatherData["features"][0]["properties"]
locationName = properties["location"]["name"]
runTime = properties["modelRunDate"]
timeSeries = properties["timeSeries"]

timeSeriesData = []
for val in timeSeries:
    time = val["time"]
    temp = val["screenTemperature"]
    feelsLikeTemp = val["feelsLikeTemperature"]
    windSpeed = val["windSpeed10m"]
    windDir = val["windDirectionFrom10m"]
    snowAmount = val["totalSnowAmount"] if "totalSnowAmount" in val else 0
    precipProb = val["probOfPrecipitation"]
    timeSeriesData.append({
        "time": time,
        "temp": temp,
        "feelsLikeTemp": feelsLikeTemp,
        "windSpeed": windSpeed,
        "windDir": windDir,
        "snowAmount": snowAmount,
        "precipProb": precipProb
    })

updatedWeather = {
    "locationName": locationName,
    "runTime": runTime,
    "timeSeries": timeSeriesData
}

dataJson["displayed"] = False
dataJson["weather"] = updatedWeather

utils.writeData(dataJson)
