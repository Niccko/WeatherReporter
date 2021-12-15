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
from threading import Thread


import database as db
import datetime as dt

load_dotenv()
api_key = os.getenv("API_KEY")
location = os.getenv("LOCATION")
CURRENT_URL = f"http://api.worldweatheronline.com/premium/v1/weather.ashx?key={api_key}&date=today&q={location}&format=json&num_of_days=0&fx=no"
HISTORY_URL = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&date={}&q={}&format=json&tp=24"

features = ["maxtempC", "mintempC", "avgtempC",
            "sunHour", "DewPointC", "humidity"]

presentation_data = {
    "updated_act": "1970-01-01",
    "updated_fst": "1970-01-01",
    "source": "actual",
    "temp": 0,
    "wind_speed": 0,
    "wind_degree": 0,
    "feels_like": 0,
    "cloud_cover": 0,
    "forecast_temp_C": 0
}

subscribers = []

current_day_data = {
    "date": "",
    "maxtempC": 100,
    "mintempC": -100,
    "avgtempC": 0,
    "sunHour": 0,
    "DewPointC": 0,
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

def add_subscriber(sub):
    subscribers.append(sub)

def notify():
    for s in subscribers:
        s(presentation_data)

def fetch_data():
    call_time = dt.datetime.now().strftime("%Y-%m-%d")
    data = requests.get(CURRENT_URL).json().get(
        "data").get("current_condition")[0]
    day_data = requests.get(HISTORY_URL.format(
        api_key, call_time, location)).json().get("data").get("weather")[0]
    
    current_day_data["mintempC"] = day_data.get("mintempC")
    current_day_data["maxtempC"] = day_data.get("maxtempC")
    current_day_data["avgtempC"] = day_data.get("avgtempC")
    current_day_data["sunHour"] = day_data.get("sunHour")
    current_day_data["DewPointC"] = day_data.get("hourly")[0].get("DewPointC")
    current_day_data["humidity"] = day_data.get("hourly")[0].get("humidity")
    current_day_data["date"] = call_time
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
            presentation_data["updated_act"] = call_time.strftime("%Y-%m-%d %I:%M:%S%p")
    except:
        data = db.get_last_data(call_time)
        history = collapse_weather_data(data)
        presentation_data["temp"] = round(model.predict(history)[0],2)
        presentation_data["source"] = "prediction"
        presentation_data["updated_fst"] = call_time.strftime("%Y-%m-%d %I:%M:%S%p")
    data = db.get_last_data(call_time+dt.timedelta(days=1))
    history = collapse_weather_data(data)
    presentation_data["forecast_temp_C"] = round(model.predict(history)[0],2)
    pprint(presentation_data)
    notify()
    

run = True

def start():
    global run
    print("Starting...")
    run = True

def stop():
    global run
    print("Stopping...")
    run = False


def main():
    schedule.every(10).seconds.do(t_get_presentation_data)
    t_get_presentation_data()
    while run:
        schedule.run_pending()
        time.sleep(1)

t = Thread(target=main)
t.start()