import json

def readData():
    dataFileRead = open("data.json", "r")
    dataJson = json.loads(dataFileRead.read())
    dataFileRead.close()
    return dataJson

def writeData(data):
    dataFileWrite = open("data.json", "w+")
    dataFileWrite.write(json.dumps(data))
    dataFileWrite.close()
