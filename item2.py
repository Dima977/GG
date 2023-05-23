from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_item2(object):
    def setupUi(self, item2):
        item2.setObjectName("item2")
        item2.resize(400, 284)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item2.setFont(font)

        self.verticalLayout = QtWidgets.QVBoxLayout(item2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.widget = QtWidgets.QGroupBox(item2)
        self.widget.setMinimumSize(QtCore.QSize(280, 200))
        self.widget.setStyleSheet("""
            QGroupBox {
                background-color: transparent;
                border: none;
            }
            QLabel#label {
                background-position: center;
                background-repeat: no-repeat;
            }
            QPushButton#btn_delete {
                background-color: #E42A2A;
                border: 2px solid red;
                border-radius: 10px;
                color: white;
            }
            QPushButton#btn_delete:hover {
                background-color: red;
                border: 2px solid red;
            }
        """)
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание по центру

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(200, 200))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMinimumSize(QtCore.QSize(300, 30))

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 3)

        self.btn_delete = QtWidgets.QPushButton(self.widget)
        self.label_2.setStyleSheet("color: white;")
        self.btn_delete.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_delete.setFont(font)
        self.btn_delete.setObjectName("btn_delete")
        self.gridLayout.addWidget(self.btn_delete, 2, 1, 1, 1)

        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(item2)
        QtCore.QMetaObject.connectSlotsByName(item2)

    def retranslateUi(self, item2):
        _translate = QtCore.QCoreApplication.translate
        item2.setWindowTitle(_translate("item2", "Form"))
        self.btn_delete.setText(_translate("item2", "Удалить"))
        self.label_2.setText(_translate("item2", "TextLabel"))
