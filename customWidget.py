from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CustomWidget(object):
    def setupUi(self, CustomWidget):
        CustomWidget.setObjectName("CustomWidget")
        CustomWidget.resize(400, 284)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        CustomWidget.setFont(font)

        self.verticalLayout = QtWidgets.QVBoxLayout(CustomWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.groupBox = QtWidgets.QGroupBox(CustomWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(280, 200))
        self.groupBox.setStyleSheet("""
            QGroupBox {
                background-color: transparent;
                border: none;
            }
            QLabel#square_label {
                background-color: #E42A2A;
                border-radius: 5px;
                min-width: 50px;
                max-width: 50px;
            }
            QPushButton#btn_link {
                background-color: #0078D7;
                border: 2px solid #0078D7;
                border-radius: 10px;
                color: white;
            }
            QPushButton#btn_link:hover {
                background-color: #0064B0;
                border: 2px solid #0064B0;
            }
        """)
        self.groupBox.setObjectName("groupBox")

        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание по центру

        self.square_label = QtWidgets.QLabel(self.groupBox)
        self.square_label.setMinimumSize(QtCore.QSize(50, 50))
        self.square_label.setMaximumSize(QtCore.QSize(50, 50))
        self.square_label.setObjectName("square_label")
        self.gridLayout.addWidget(self.square_label, 0, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(300, 30))

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.gridLayout.addItem(spacer_item, 0, 2, 1, 1)

        self.btn_link = QtWidgets.QPushButton(self.groupBox)
        self.label_2.setStyleSheet("color: white;")
        self.btn_link.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_link.setFont(font)
        self.btn_link.setObjectName("btn_link")
        self.gridLayout.addWidget(self.btn_link, 0, 3, 1, 1)

        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(CustomWidget)
        QtCore.QMetaObject.connectSlotsByName(CustomWidget)

    def retranslateUi(self, CustomWidget):
        _translate = QtCore.QCoreApplication.translate
        CustomWidget.setWindowTitle(_translate("CustomWidget", "Form"))
        self.btn_link.setText(_translate("CustomWidget", "Link"))
        self.label_2.setText(_translate("CustomWidget", "TextLabel"))
