import os
import csv
import requests
from dotenv import load_dotenv
from pprint import pprint
import datetime
from calendar import monthrange
import time
import json
import pandas as pd
load_dotenv()

api_key = os.getenv("API_KEY")

BASE_URL = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&date={}&q={}&format=json&tp=12&enddate={}"
START_DATE = datetime.datetime.strptime('01-01-2010','%d-%m-%Y').date()
END_DATE = datetime.datetime.strptime('30-10-2021','%d-%m-%Y').date()

def drop_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

with open('resources/daily.csv', 'a', newline='') as daily_weather:
    fieldnames_daily = ['date', "sunrise", 'sunset', 'moonrise',
                        'moonset', 'moon_phase', 'moon_illumination',
                        'maxtempC', 'mintempC', 'avgtempC', 'totalSnow_cm',
                        'sunHour', "uvIndex"]
    writer_daily = csv.DictWriter(daily_weather, fieldnames=fieldnames_daily)
    with open('resources/hourly.csv', 'a') as hourly_weather:
        fieldnames_hourly = ['date','time', 'tempC', 'windspeedKmph', "winddirDegree",
                             'weatherDesc', 'precipMM', 'humidity', 'visibility', 'pressure',
                             'cloudcover', 'HeatIndexC', 'DewPointC', 'WindChillC', 'WindGustKmph',
                             'FeelsLikeC']

        writer_hourly = csv.DictWriter(
            hourly_weather, fieldnames=fieldnames_hourly)

        writer_daily.writeheader()
        writer_hourly.writeheader()

        cur_date = START_DATE
        while cur_date<END_DATE:
            print(cur_date)
            last_day = cur_date+datetime.timedelta(days=monthrange(cur_date.year, cur_date.month)[1])-datetime.timedelta(days=1)
            data_url = BASE_URL.format(api_key,cur_date,"Moscow, Russia", str(last_day))
            data_monthly = requests.get(data_url).json().get("data").get("weather")
            for data in data_monthly:
                daily_data = {}
                daily_data["date"] = data.get("date")
                daily_data["sunrise"] = data.get("astronomy")[0].get("sunrise")
                daily_data["sunset"] = data.get("astronomy")[0].get("sunset")
                daily_data["moonrise"] = data.get("astronomy")[0].get("moonrise")
                daily_data["moonset"] = data.get("astronomy")[0].get("moonset")
                daily_data["moon_phase"] = data.get("astronomy")[0].get("moon_phase")
                daily_data["moon_illumination"] = data.get("astronomy")[0].get("moon_illumination")
                daily_data["maxtempC"] = data.get("maxtempC")
                daily_data["mintempC"] = data.get("mintempC")
                daily_data["avgtempC"] = data.get("avgtempC")
                daily_data["totalSnow_cm"] = data.get("totalSnow_cm")
                daily_data["sunHour"] = data.get("sunHour")
                daily_data["uvIndex"] = data.get("uvIndex")
                

                for data_h in data.get("hourly"):
                    hourly_data = {}
                    hourly_data["date"] = data.get("date")
                    hourly_data["time"] = data_h.get("time")
                    hourly_data["tempC"] = data_h.get("tempC")
                    hourly_data["windspeedKmph"] = data_h.get("windspeedKmph")
                    hourly_data["winddirDegree"] = data_h.get("winddirDegree")
                    hourly_data["weatherDesc"] = data_h.get("weatherDesc")[0].get("value")
                    hourly_data["precipMM"] = data_h.get("precipMM")
                    hourly_data["humidity"] = data_h.get("humidity")
                    hourly_data["visibility"] = data_h.get("visibility")
                    hourly_data["pressure"] = data_h.get("pressure")
                    hourly_data["cloudcover"] = data_h.get("cloudcover")
                    hourly_data["HeatIndexC"] = data_h.get("HeatIndexC")
                    hourly_data["DewPointC"] = data_h.get("DewPointC")
                    hourly_data["WindChillC"] = data_h.get("WindChillC")
                    hourly_data["WindGustKmph"] = data_h.get("WindGustKmph")
                    hourly_data["FeelsLikeC"] = data_h.get("FeelsLikeC")
                    writer_hourly.writerow(hourly_data)

                writer_daily.writerow(daily_data)
            cur_date+=datetime.timedelta(days=monthrange(cur_date.year, cur_date.month)[1])
            time.sleep(1)


