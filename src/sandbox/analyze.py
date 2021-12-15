import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

parser = lambda date: dt.strptime(date, '%Y-%m-%d')
weather_d = pd.read_csv("resources/daily.csv", parse_dates=[0], date_parser=parser)
weather_h = pd.read_csv("resources/hourly.csv", parse_dates=[0], date_parser=parser)
weather_h = weather_h[weather_h.time==1200]

# joined = weather_d.merge(weather_h, on="date")
# features = joined.columns.drop(["tempC","WindGustKmph","windspeedKmph","winddirDegree","precipMM", "visibility","pressure","WindChillC","HeatIndexC",
#                                   "uvIndex","time", "sunrise", "FeelsLikeC", "weatherDesc", "sunset", "moonrise",
#                                       "moonset","moon_phase","moon_illumination", "totalSnow_cm", "cloudcover"])
# joined = joined[features]
# for i in range(1,4):
#     for f in features:
#         if f != "date":
#             joined[f'{f}_lg{i}'] = joined[f].shift(i)
# joined.to_csv("resources/pre_training.csv")



# corr_values = data.corr()[['avgtempC']].sort_values('avgtempC')
# print(corr_values[abs(corr_values["avgtempC"])>0.6])


data = pd.read_csv("resources/pre_training.csv")
fig_1, axes_1 = plt.subplots(nrows=3, ncols=3)
fig_2, axes_2 = plt.subplots(nrows=3, ncols=3)
features_p1 = ["humidity","sunHour","DewPointC"]
features_p2 = ["maxtempC","mintempC","avgtempC"]
for i,f in enumerate(features_p1):
    for j in range(3):
        data.plot(ax=axes_1[i,j],kind="scatter",y="avgtempC",x=f+f"_lg{i+1}")

for i,f in enumerate(features_p2):
    for j in range(3):
        data.plot(ax=axes_2[i,j],kind="scatter",y="avgtempC",x=f+f"_lg{i+1}")
plt.show()