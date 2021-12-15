
import sys
from PyQt5 import QtWidgets
import design
import requests
import os
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from main import add_subscriber, start, stop


dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class WeatherApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        start()
        self.setupUi(self)

    def update(self,data):
        self.temp.setText(f"Temperature: {round(float(data.get('temp')),2)} °С")
        self.wind_degree.setText(f"Wind degree: {data.get('wind_degree')}°")
        self.wind_speed.setText(f"Wind speed: {data.get('wind_speed')} kmp/h")
        self.feels_like.setText(f"Feels like: {data.get('feels_like')} °C")
        #print(data.get("cloud_cover"))
        self.cloud_cover.setText(f"Cloud cover: {data.get('cloud_cover')}%")
        self.upd_actual.setText(f"Last actual update: {data.get('updated_act')}")
        self.upd_fst.setText(f"Last forecast update: {data.get('updated_fst')}")
        self.state.setText(f"{data.get('source')}".upper())
        self.forecast.setText(f"Forecast: {round(float(data.get('forecast_temp_C')),2)} °С")

    def closeEvent(self, event):
        stop()
        


def main():
    def update(data):
        window.update(data)
    app = QtWidgets.QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    add_subscriber(update)
    app.exec_()


if __name__ == '__main__':
    main()
