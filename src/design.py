# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/design.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(295, 309)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.upd_actual = QtWidgets.QLabel(self.centralwidget)
        self.upd_actual.setGeometry(QtCore.QRect(10, 30, 271, 16))
        self.upd_actual.setObjectName("upd_actual")
        self.temp = QtWidgets.QLabel(self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(10, 70, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.temp.setFont(font)
        self.temp.setObjectName("temp")
        self.forecast = QtWidgets.QLabel(self.centralwidget)
        self.forecast.setGeometry(QtCore.QRect(10, 110, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.forecast.setFont(font)
        self.forecast.setObjectName("forecast")
        self.wind_speed = QtWidgets.QLabel(self.centralwidget)
        self.wind_speed.setGeometry(QtCore.QRect(10, 140, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.wind_speed.setFont(font)
        self.wind_speed.setObjectName("wind_speed")
        self.wind_degree = QtWidgets.QLabel(self.centralwidget)
        self.wind_degree.setGeometry(QtCore.QRect(10, 170, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.wind_degree.setFont(font)
        self.wind_degree.setObjectName("wind_degree")
        self.cloud_cover = QtWidgets.QLabel(self.centralwidget)
        self.cloud_cover.setGeometry(QtCore.QRect(10, 200, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cloud_cover.setFont(font)
        self.cloud_cover.setObjectName("cloud_cover")
        self.feels_like = QtWidgets.QLabel(self.centralwidget)
        self.feels_like.setGeometry(QtCore.QRect(10, 230, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.feels_like.setFont(font)
        self.feels_like.setObjectName("feels_like")
        self.upd_fst = QtWidgets.QLabel(self.centralwidget)
        self.upd_fst.setGeometry(QtCore.QRect(10, 50, 271, 16))
        self.upd_fst.setObjectName("upd_fst")
        self.state = QtWidgets.QLabel(self.centralwidget)
        self.state.setGeometry(QtCore.QRect(100, 10, 111, 20))
        self.state.setObjectName("state")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 295, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upd_actual.setText(_translate("MainWindow", "Last actual update:"))
        self.temp.setText(_translate("MainWindow", "Temperature:"))
        self.forecast.setText(_translate("MainWindow", "Forecast:"))
        self.wind_speed.setText(_translate("MainWindow", "Wind speed: "))
        self.wind_degree.setText(_translate("MainWindow", "Wind degree:"))
        self.cloud_cover.setText(_translate("MainWindow", "Cloud cover:"))
        self.feels_like.setText(_translate("MainWindow", "Feels like:"))
        self.upd_fst.setText(_translate("MainWindow", "Last forecast update:"))
        self.state.setText(_translate("MainWindow", "ACTUAL"))