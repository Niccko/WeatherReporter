from os import name
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
from datetime import datetime as dt
import itertools as IT
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import os

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
x = data.iloc[:, 8:]
y = data["avgtempc"]

x_train, x_temp, y_train, y_temp = train_test_split(x,y,test_size=0.2, random_state=23)
x_test, x_valid, y_test, y_valid = train_test_split(x_temp,y_temp,test_size=0.5, random_state=23)

# print("Training instances   {}, Training features   {}".format(x_train.shape[0], x_train.shape[1]))
# print("Validation instances {}, Validation features {}".format(x_valid.shape[0], x_valid.shape[1]))
# print("Testing instances    {}, Testing features    {}".format(x_test.shape[0], x_test.shape[1]))


def input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.compat.v1.estimator.inputs.pandas_input_fn(x=X,
                                                         y=y,
                                                         num_epochs=num_epochs,
                                                         shuffle=shuffle,
                                                         batch_size=batch_size)


feature_cols = [tf.feature_column.numeric_column(col) for col in x.columns]

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                      hidden_units=[50, 50],
                                      model_dir='weather_model')

# evaluations = []
# STEPS = 400
# for i in range(200):
#     print(f"STEP: {i}")
#     regressor.train(input_fn=wx_input_fn(x_train, y=y_train), steps=STEPS)
#     evaluations.append(regressor.evaluate(input_fn=wx_input_fn(x_valid,
#                                                                y_valid,
#                                                                num_epochs=1,
#                                                                shuffle=False)))

# loss_values = [ev['loss'] for ev in evaluations]
# training_steps = [ev['global_step'] for ev in evaluations]

# pprint(evaluations)

# x_pred = x_test.iloc[[0]]
# y_pred = y_test.iloc[[0]]
# print(x_pred)
# print(y_pred)

# pred = regressor.predict(input_fn=wx_input_fn(x_test,
#                                               num_epochs=1,
#                                               shuffle=False))
# predictions = np.array([p['predictions'][0] for p in pred])

# print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(y_test, predictions))
# print("The Median Absolute Error: %.2f degrees Celcius" % median_absolute_error(y_test, predictions))


def predict(data):
    prediction = regressor.predict(input_fn=wx_input_fn(
        data,
        num_epochs=1,
        shuffle=False
    ))
    print(data)
    return np.array([p['predictions'][0] for p in prediction])


    
