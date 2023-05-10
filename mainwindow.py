# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: #535252;\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(20, 190, 300, 800))
        self.widget.setStyleSheet("background-color:  #2D2727;\n"
"border-radius: 10px;")
        self.widget.setObjectName("widget")
        self.btn_CPU = QtWidgets.QPushButton(self.widget)
        self.btn_CPU.setGeometry(QtCore.QRect(30, 60, 240, 65))
        self.btn_CPU.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_CPU.setObjectName("btn_CPU")
        self.btn_GPU = QtWidgets.QPushButton(self.widget)
        self.btn_GPU.setGeometry(QtCore.QRect(30, 140, 240, 65))
        self.btn_GPU.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_GPU.setObjectName("btn_GPU")
        self.btn_RAM = QtWidgets.QPushButton(self.widget)
        self.btn_RAM.setGeometry(QtCore.QRect(30, 300, 240, 65))
        self.btn_RAM.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_RAM.setObjectName("btn_RAM")
        self.btn_motherboard = QtWidgets.QPushButton(self.widget)
        self.btn_motherboard.setGeometry(QtCore.QRect(30, 220, 240, 65))
        self.btn_motherboard.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_motherboard.setObjectName("btn_motherboard")
        self.btn_storage_device = QtWidgets.QPushButton(self.widget)
        self.btn_storage_device.setGeometry(QtCore.QRect(30, 380, 240, 65))
        self.btn_storage_device.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_storage_device.setObjectName("btn_storage_device")
        self.btn_power_unit = QtWidgets.QPushButton(self.widget)
        self.btn_power_unit.setGeometry(QtCore.QRect(30, 460, 240, 65))
        self.btn_power_unit.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_power_unit.setObjectName("btn_power_unit")
        self.btn_cooling = QtWidgets.QPushButton(self.widget)
        self.btn_cooling.setGeometry(QtCore.QRect(30, 540, 240, 65))
        self.btn_cooling.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_cooling.setObjectName("btn_cooling")
        self.btn_case = QtWidgets.QPushButton(self.widget)
        self.btn_case.setGeometry(QtCore.QRect(30, 620, 240, 65))
        self.btn_case.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_case.setObjectName("btn_case")
        self.btn_help = QtWidgets.QPushButton(self.widget)
        self.btn_help.setGeometry(QtCore.QRect(100, 720, 93, 28))
        self.btn_help.setObjectName("btn_help")
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setGeometry(QtCore.QRect(1490, 10, 400, 970))
        self.widget_2.setStyleSheet("background-color:  #2D2727;\n"
"border-radius: 10px;")
        self.widget_2.setObjectName("widget_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.widget_2)
        self.scrollArea_2.setGeometry(QtCore.QRect(20, 290, 361, 651))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 361, 651))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.layout_2 = QtWidgets.QVBoxLayout()
        self.layout_2.setObjectName("layout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.layout_2.addWidget(self.label_3)
        self.layout_CPU = QtWidgets.QVBoxLayout()
        self.layout_CPU.setContentsMargins(30, 30, -1, -1)
        self.layout_CPU.setObjectName("layout_CPU")
        self.layout_2.addLayout(self.layout_CPU)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setObjectName("label_4")
        self.layout_2.addWidget(self.label_4)
        self.layout_GPU = QtWidgets.QVBoxLayout()
        self.layout_GPU.setContentsMargins(-1, 30, -1, -1)
        self.layout_GPU.setObjectName("layout_GPU")
        self.layout_2.addLayout(self.layout_GPU)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName("label_5")
        self.layout_2.addWidget(self.label_5)
        self.layout_motherboard = QtWidgets.QVBoxLayout()
        self.layout_motherboard.setContentsMargins(-1, 30, -1, -1)
        self.layout_motherboard.setObjectName("layout_motherboard")
        self.layout_2.addLayout(self.layout_motherboard)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem3)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_6.setObjectName("label_6")
        self.layout_2.addWidget(self.label_6)
        self.layout_RAM = QtWidgets.QVBoxLayout()
        self.layout_RAM.setContentsMargins(-1, 30, -1, -1)
        self.layout_RAM.setObjectName("layout_RAM")
        self.layout_2.addLayout(self.layout_RAM)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem4)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_7.setObjectName("label_7")
        self.layout_2.addWidget(self.label_7)
        self.layout_power_unit = QtWidgets.QVBoxLayout()
        self.layout_power_unit.setContentsMargins(-1, 30, -1, -1)
        self.layout_power_unit.setObjectName("layout_power_unit")
        self.layout_2.addLayout(self.layout_power_unit)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem5)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_8.setObjectName("label_8")
        self.layout_2.addWidget(self.label_8)
        self.layout_cooling = QtWidgets.QVBoxLayout()
        self.layout_cooling.setContentsMargins(-1, 30, -1, -1)
        self.layout_cooling.setObjectName("layout_cooling")
        self.layout_2.addLayout(self.layout_cooling)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem6)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_9.setObjectName("label_9")
        self.layout_2.addWidget(self.label_9)
        self.layout_case = QtWidgets.QVBoxLayout()
        self.layout_case.setContentsMargins(-1, 30, -1, -1)
        self.layout_case.setObjectName("layout_case")
        self.layout_2.addLayout(self.layout_case)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem7)
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_10.setObjectName("label_10")
        self.layout_2.addWidget(self.label_10)
        self.layout_storage_device = QtWidgets.QVBoxLayout()
        self.layout_storage_device.setContentsMargins(-1, 30, -1, -1)
        self.layout_storage_device.setObjectName("layout_storage_device")
        self.layout_2.addLayout(self.layout_storage_device)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_2.addItem(spacerItem8)
        self.gridLayout_4.addLayout(self.layout_2, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(20, 100, 81, 31))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(50, 180, 305, 50))
        self.pushButton.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(20, 256, 161, 20))
        self.label_2.setObjectName("label_2")
        self.btn_clear = QtWidgets.QPushButton(self.widget_2)
        self.btn_clear.setGeometry(QtCore.QRect(280, 250, 93, 28))
        self.btn_clear.setStyleSheet("background-color: #E42A2A;\n"
"border-radius: 10px;")
        self.btn_clear.setObjectName("btn_clear")
        self.widget_3 = QtWidgets.QWidget(self.frame)
        self.widget_3.setGeometry(QtCore.QRect(430, 10, 1000, 250))
        self.widget_3.setStyleSheet("background-color:  #2D2727;\n"
"border-radius: 10px;")
        self.widget_3.setObjectName("widget_3")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(429, 289, 1000, 700))
        self.frame_2.setStyleSheet("background-color:  #2D2727;\n"
"border-radius: 10px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 978, 678))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.gridLayout_3.addLayout(self.layout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.btn_exit = QtWidgets.QPushButton(self.frame)
        self.btn_exit.setGeometry(QtCore.QRect(20, 10, 301, 141))
        self.btn_exit.setStyleSheet("QPushButton{\n"
"background-color:  #D9D9D9;\n"
"border-radius: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                       stop: 0 #dadbde, stop: 1 #f6f7fa);\n"
"    text: Выход; \n"
" }")
        self.btn_exit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/izobrazhenie-PhotoRoom_png-PhotoRoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exit.setIcon(icon)
        self.btn_exit.setIconSize(QtCore.QSize(200, 250))
        self.btn_exit.setObjectName("btn_exit")
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
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
        self.btn_CPU.setText(_translate("MainWindow", "Процессор"))
        self.btn_GPU.setText(_translate("MainWindow", "Видеокарта"))
        self.btn_RAM.setText(_translate("MainWindow", "Оперативная память"))
        self.btn_motherboard.setText(_translate("MainWindow", "Материнская плата"))
        self.btn_storage_device.setText(_translate("MainWindow", "Накопители"))
        self.btn_power_unit.setText(_translate("MainWindow", "Блок питания"))
        self.btn_cooling.setText(_translate("MainWindow", "Охлаждение"))
        self.btn_case.setText(_translate("MainWindow", "Корпус"))
        self.btn_help.setText(_translate("MainWindow", "Помощь!"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Процессор:</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Видеокарта:</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Материнская плата:</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">ОЗУ:</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Блок питания:</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Охлаждение:</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Корпус:</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Накопители:</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Цена:"))
        self.pushButton.setText(_translate("MainWindow", "Сформировать"))
        self.label_2.setText(_translate("MainWindow", "Конфигурация:"))
        self.btn_clear.setText(_translate("MainWindow", "Очистить"))
