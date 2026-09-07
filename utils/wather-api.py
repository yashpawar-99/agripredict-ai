import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import date

import requests


#use for convert location to the latitude and longitude 

def get_coordinates(location):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return None, None

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    return latitude, longitude

#use for to farmer select the season and it passes a date to wather api to fached historical data 


def get_season_dates(season):
    today = date.today()
    year = today.year

    season = season.strip().title()

    if season == "Kharif":
        start_date = date(year, 6, 1)
        end_date = date(year, 10, 31)

    elif season == "Rabi":
        start_date = date(year, 11, 1)
        end_date = date(year + 1, 3, 31)

    elif season == "Summer":
        start_date = date(year, 3, 1)
        end_date = date(year, 5, 31)

    elif season == "Autumn":
        start_date = date(year, 9, 1)
        end_date = date(year, 11, 30)

    elif season == "Winter":
        start_date = date(year, 11, 1)
        end_date = date(year + 1, 2, 28)

    elif season == "Whole Year":
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

    else:
        raise ValueError("Invalid season")

    # If season contains future dates
    # use the previous years season
    if end_date >= today:
        year -= 1

        if season == "Kharif":
            start_date = date(year, 6, 1)
            end_date = date(year, 10, 31)

        elif season == "Rabi":
            start_date = date(year, 11, 1)
            end_date = date(year + 1, 3, 31)

        elif season == "Summer":
            start_date = date(year, 3, 1)
            end_date = date(year, 5, 31)

        elif season == "Autumn":
            start_date = date(year, 9, 1)
            end_date = date(year, 11, 30)

        elif season == "Winter":
            start_date = date(year, 11, 1)
            end_date = date(year + 1, 2, 28)

        elif season == "Whole Year":
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

    return start_date.isoformat(), end_date.isoformat()

#----------------------------------------------------------------------------------

# input the feature and passed output to wather API to faced data 

season = input("Enter season: ")
district = input("Enter DIstrict : ")
state = input("Enter state : ")

start_date, end_date = get_season_dates(season)

latitude, longitude = get_coordinates(f"{district},{state},india")

print("Start Date:", start_date)
print("End Date:", end_date)
print("Latitude:", latitude)
print("Longitude:", longitude)

#-------------------------------------------------------------------------------------
#API boiler plate code -

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://historical-forecast-api.open-meteo.com/v1/forecast"


params = {
	"latitude": latitude,
	"longitude": longitude,
	"start_date": start_date,
	"end_date": end_date,
	"daily": "rain_sum",
	"hourly": ["temperature_2m", "relative_humidity_1000hPa", "relative_humidity_100hPa"],
	"timezone": "auto",
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_1000hPa = hourly.Variables(1).ValuesAsNumpy()
hourly_relative_humidity_100hPa = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_1000hPa"] = hourly_relative_humidity_1000hPa
hourly_data["relative_humidity_100hPa"] = hourly_relative_humidity_100hPa

hourly_dataframe = pd.DataFrame(data = hourly_data)
#print("\nHourly data\n", hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_rain_sum = daily.Variables(0).ValuesAsNumpy()

daily_data = {
	"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

daily_data["rain_sum"] = daily_rain_sum

daily_dataframe = pd.DataFrame(data = daily_data)
#print("\nDaily data\n", daily_dataframe)

#----------------------------------------------------------------------------------------------
#Output : 
#daily rainfall 

rainfall_30_days = daily_data["rain_sum"][-30:].sum()
print(f"Rainfall (last 30 days) for crop recomendation : {rainfall_30_days:.2f} mm")

#houarly values 

print(f"temperature_2m : {hourly_dataframe["temperature_2m"].mean()}")
print(f"relative_humidity_1000hpa for  crop recomendation : {hourly_data["relative_humidity_1000hPa"].mean()}")
print(f"relative_humidity_100hpa for  crop yeild  :{hourly_data["relative_humidity_100hPa"].mean()}")

#---------------------------------------------------------------------------------------------------