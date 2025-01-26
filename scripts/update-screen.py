import utils

# job 1: pull in data.json file, see if there are any changes from last time it ran
# job 2 (for when I've got the Raspberry Pi): update the screen

dataJson = utils.readData()

if dataJson["displayed"]:
    print("do nothing")
    # do nothing
else:
    print("display data")
