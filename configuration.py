# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_configuration(object):
    def setupUi(self, configuration):
        configuration.setObjectName("configuration")
        configuration.resize(1000, 800)
        self.horizontalLayout = QtWidgets.QHBoxLayout(configuration)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QtWidgets.QScrollArea(configuration)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 976, 776))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.horizontalLayout_2.addLayout(self.layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.retranslateUi(configuration)
        QtCore.QMetaObject.connectSlotsByName(configuration)

    def retranslateUi(self, configuration):
        _translate = QtCore.QCoreApplication.translate
        configuration.setWindowTitle(_translate("configuration", "Form"))
