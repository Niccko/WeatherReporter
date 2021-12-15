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
def input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.compat.v1.estimator.inputs.pandas_input_fn(x=X,
                                                         y=y,
                                                         num_epochs=num_epochs,
                                                         shuffle=shuffle,
                                                         batch_size=batch_size)

def predict(data):
    prediction = regressor.predict(input_fn=input_fn(
        data,
        num_epochs=1,
        shuffle=False
    ))
    print(data)
    return np.array([p['predictions'][0] for p in prediction])


data = pd.read_csv("resources/pre_training.csv")
x = data.iloc[:, 8:]
y = data["avgtempC"]

# x_train, x_temp, y_train, y_temp = train_test_split(
#     x, y, test_size=0.2, random_state=23)
# x_test, x_valid, y_test, y_valid = train_test_split(
#     x_temp, y_temp, test_size=0.5, random_state=23)

# print("Training instances   {}, Training features   {}".format(
#     x_train.shape[0], x_train.shape[1]))
# print("Validation instances {}, Validation features {}".format(
#     x_valid.shape[0], x_valid.shape[1]))
# print("Testing instances    {}, Testing features    {}".format(
#     x_test.shape[0], x_test.shape[1]))





feature_cols = [tf.feature_column.numeric_column(col) for col in x.columns]

regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                      hidden_units=[25, 25],
                                      model_dir='weather_model')

# evaluations = []
# STEPS = 400
# for i in range(15):
#     print(f"STEP: {i}",end=" | ")
#     regressor.train(input_fn=input_fn(x_train, y=y_train), steps=STEPS)
#     eval = regressor.evaluate(input_fn=input_fn(x_valid,
#                                                 y_valid,
#                                                 num_epochs=1,
#                                                 shuffle=False))
#     print("Loss: "+str(eval["loss"]))
#     evaluations.append(eval)

# loss_values = [ev['loss'] for ev in evaluations]
# training_steps = [ev['global_step'] for ev in evaluations]

# plt.plot(training_steps, loss_values)
# plt.xlabel("Training steps")
# plt.ylabel("Loss")
# plt.show()

# x_pred = x_test.iloc[[0]]
# y_pred = y_test.iloc[[0]]
# print(x_pred)
# print(y_pred)

# pred = regressor.predict(input_fn=input_fn(x_test,
#                                               num_epochs=1,
#                                               shuffle=False))
# predictions = np.array([p['predictions'][0] for p in pred])

# print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(y_test, predictions))
# print("The Median Absolute Error: %.2f degrees Celcius" % median_absolute_error(y_test, predictions))

