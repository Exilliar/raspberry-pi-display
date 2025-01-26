# Python Scripts for Raspberry Pi

A collection of Python scripts that I have written for my Raspberry Pi project (may later contain more than just scripts).

A [Raspberry Pi 4b](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) is being used and the [5.83" E-Ink Display HAT For Raspberry Pi (648×480)](https://thepihut.com/products/5-83-e-ink-display-hat-for-raspberry-pi-648x480?variant=38122006184131) eInk screen is being used as a display.

## Setup

### Packages

All required packages are in the `requirements.txt` file.

### The `scripts/data.json` file

This file contains both the config values for the scripts and is also the location that all of the scripts will write their data to.

This file needs to contain exact long-lat information, so only a template (`data-template.json`) is provided in the repo. When running these scripts a new `data.json` file should be created, with the `config` values updated to match.

### Env file

There is a `.env-template` file that needs to be filled into a `.env` file. The keys for the various API's (minus the diary API) can be found in the links to the API's described below.

### Diary API

This API is my own personal one, therefore it cannot be accessed by anyone but me. Any reference to the diary API (including the script) can be deleted.

## Scripts

All the below scripts can be found in the `scripts` folder.

### diary-title.py

A script that makes a call out to my diary server to get the title of the current day.

The `datetime` format for the datetime that needs to be passed to the diary api can be found in the `data.json` file config -> diary -> datetimeFormat.

The title is saved to the `data.json` output -> diary -> title string.

### tfl-data.py

Gets the status of the tube lines to display from the [tfl api](https://api-portal.tfl.gov.uk/).

Which lines it gets the status of can be set in the `data.json` config -> tfl -> lines array.

The data is output to the `data.json` output -> tfl object. Each line will have it's own object.

### weather-data.py

Gets the weather data from the [Met Office API - Site-Specific forecast - Global spot API](https://datahub.metoffice.gov.uk/docs/f/category/site-specific/overview).

The config is in the `data.json` config -> weather object.

This can control the location that is used. The available locations are in the `locations` object. Each location must have a name (this should be the key) and a lat-long. Which location is used is controlled through the `selectedLocation`. This should be set to the key of the selected location.

Whether the forecast is given as `hours`, `three-hourly`, or `daily` is controlled by the `selectedTimestep` variable. This value should be the index in the `availableTimesteps` array that the forecast should be set to.

The `datetime` format for the datetimes given are in the `datetimeFormat` variable. This can be passed into `datetime.strptime` function to convert the `datetime` string into a `datetime` object.

The output is stored in output -> weather.

The time the forecast was run on is in the variable `runTime`.

The location that was used to get the forecast is in the variable `locationName`.

The timeseries data for the forecast is in the `timeSeries` array. The variable names are hopefully self-explanatory.

### update-screen.py

The script that will update the content shown on the screen. It will get the content from the `data.json` file.

Before updating the screen it will check the `displayed` boolean in the `data.json` file to check whether the screen needs to update. When each script runs it will update this value to be `false` so that this script knows to run. Currently, every script will always set this value to `false`, regardless of whether it actually ends up making any changes. However, eventually the scripts may be updated to only update this value when a change has actually been made. This will mean that the screen may not need to update as regularly. This is desirable as the screen will take ~5 seconds to update and will only consume power when updating.

### utils.py

Script containing some generic util functions that most of the other scripts will use. This mainly has to do with opening and editting the `data.json` files.

## Project plan

### V1 - current stage

In V1 of this project all of the scripts will be set up on os-level timers to run at set intervals. The `update-screen.py` script will run to update the screen.

### V2

In V2 the Raspberry Pi will be updated to run a [Flask server](https://flask.palletsprojects.com/en/stable/). This will allow for the management of timing script runs to be handled by the server and also provide a backend to allow for changing the values in the config section of the `data.json` file.

A React app may also be made in this stage to give easier control over what is being displayed.

### V3

A step count will be added to the display. This will likely be the most difficult step as it will require making an app for phones which will run every X hours and push out the step count data to the Raspberry Pi as this health data is not easily accessed through an API (unless for commercial use).

## Script timings

Every hour at :50 - `weather-data.py`
Every half hour at :55 and :25 - `tfl-data.py`
Every day at 6:00am - `diary-title.py`
Every half hour at :05 and :35 - `update-screen.py`

Timings need to be staggered as all scripts access the `data.json` file, therefore if any ran at the same time this could cause locking issues. V2 of the project with a server should hopefully be able to solve this issue by giving the server more control over when each script runs.
