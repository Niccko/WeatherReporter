from os import name
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from datetime import datetime as dt
import itertools as IT

# features = ["date", "maxtempC","mintempC", "avgtempC", "pressure", "DewPointC","humidity"]

# parser = lambda date: dt.strptime(date, '%Y-%m-%d')
# weather_d = pd.read_csv("resources/daily_full.csv", parse_dates=[0], date_parser=parser)
# weather_h = pd.read_csv("resources/hourly_full.csv", parse_dates=[0], date_parser=parser)
# weather_h = weather_h[weather_h.time==1200]

# joined = weather_d.merge(weather_h, on="date")
# joined = joined[features]
# for i in range(1,4):
#     for f in features:
#         if f != "date":
#             joined[f'{f}_lg{i}'] = joined[f].shift(i)
# joined.to_csv("resources/pre_training.csv")

data = pd.read_csv("resources/pre_training.csv")
x_train = data.iloc[:, 8:]
print(x_train.iloc[[3]])
y_train = data["avgtempC"]
print(y_train)

normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(x_train)

model = tf.keras.models.Sequential([
    normalizer,
    tf.keras.layers.Dense(10, input_shape=(18,), activation='relu'),
    #tf.keras.layers.Dense(10, activation='sigmoid'),
    tf.keras.layers.Dense(1, activation='linear', name="output")
])

print(y_train.iloc[[1]])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='mse',
              metrics=["accuracy"])


for i in range(150):
    model.fit(x_train, y_train, epochs=10, shuffle=True, batch_size=200)


while True:
    inp = int(input())
    print(model.predict(x_train.iloc[[inp]]))

