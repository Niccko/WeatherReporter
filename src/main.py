import time
from dotenv import load_dotenv
from contextlib import contextmanager
import os
import threading
import _thread
import requests
from pprint import pprint
import sandbox.model as model
import pandas as pd
import schedule


import database as db
import datetime as dt

load_dotenv()
api_key = os.getenv("API_KEY")
location = os.getenv("LOCATION")
CURRENT_URL = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&date=today&q={location}&format=json&num_of_days=0&fx=no"
HISTORY_URL = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&date={}&q={}&format=json&tp=24"

features = ["maxtempc", "mintempc", "avgtempc",
            "pressure", "dewpointc", "humidity"]

presentation_data = {
    "updated": "1970-01-01",
    "source": "actual",
    "temp": 0,
    "wind_speed": 0,
    "wind_degree": 0,
    "feels_like": 0,
    "cloud_cover": 0,
    "forecast_temp_C": 0
}

current_day_data = {
    "date": "",
    "maxtempc": 100,
    "mintempc": -100,
    "avgtempc": 0,
    "pressure": 0,
    "dewpointc": 0,
    "humidity": 0
}


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutError()
    finally:
        timer.cancel()


def fetch_data():
    call_time = dt.datetime.now().strftime("%Y-%m-%d")
    data = requests.get(CURRENT_URL).json().get(
        "data").get("current_condition")[0]
    day_data = requests.get(HISTORY_URL.format(
        api_key, call_time, location)).json().get("data").get("weather")[0]

    current_day_data["mintempc"] = day_data.get("mintempC")
    current_day_data["maxtempc"] = day_data.get("maxtempC")
    current_day_data["avgtempc"] = day_data.get("avgtempC")
    current_day_data["pressure"] = day_data.get("hourly")[0].get("pressure")
    current_day_data["dewpointc"] = day_data.get("hourly")[0].get("DewPointC")
    current_day_data["humidity"] = day_data.get("hourly")[0].get("humidity")
    current_day_data["date"] = call_time
    pprint(current_day_data)
    db.insert_current(current_day_data)
    return {
        "temp": data.get("temp_C"),
        "wind_speed": data.get("windspeedKmph"),
        "wind_degree": data.get("winddirDegree"),
        "feels_like": data.get("FeelsLikeC"),
        "cloud_cover": data.get("cloudcover")
    }


def collapse_weather_data(data):
    history = pd.DataFrame(data)
    history.sort_values("date")
    collapsed_history = {}
    for i in range(1, 4):
        for f in features:
            print(history.iloc[3-i][f])
            collapsed_history[f'{f}_lg{i}'] = history.iloc[i-1][f]
    return pd.DataFrame([collapsed_history])



def t_get_presentation_data():
    call_time = dt.datetime.now()
    try:
        with time_limit(5):
            actual_weather = fetch_data()
            for key in actual_weather:
                presentation_data[key] = actual_weather[key]
            presentation_data["source"] = "actual"
    except:
        data = db.get_last_data(call_time)
        history = collapse_weather_data(data)
        presentation_data["temp_C"] = model.predict(history)[0]
        presentation_data["source"] = "prediction"
    data = db.get_last_data(call_time+dt.timedelta(days=1))
    history = collapse_weather_data(data)
    presentation_data["forecast_temp_C"] = model.predict(history)[0]
    presentation_data["updated"] = call_time.strftime("%Y-%m-%d %I:%M%p")

schedule.every(15).minutes.do(t_get_presentation_data)

while True:
    schedule.run_pending()
    time.sleep(1)
