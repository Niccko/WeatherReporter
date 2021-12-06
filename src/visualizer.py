from matplotlib import use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

avg_temp = pd.read_csv("resources/daily.csv",parse_dates=["date"], usecols=["date","totalSnow_cm"])

plt.plot(avg_temp["date"], avg_temp["totalSnow_cm"])

plt.show()