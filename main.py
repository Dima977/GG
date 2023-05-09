from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QScrollArea, QPushButton)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from mainwindow import Ui_MainWindow
from item import Ui_item
from item2 import Ui_item2
import sqlite3
import sys

with sqlite3.connect("PR.db") as db:
    cur = db.cursor()
    db_CPU = cur.execute("""select count(CPU_ID) from CPU""").fetchall()
    image_CPU = cur.execute("""select image from CPU""").fetchall()
    name_CPU = cur.execute("""select name from CPU""").fetchall()
    db_GPU = cur.execute("""select count(GPU_ID) from GPU""").fetchall()
    db_motherboard = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    db_RAM = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    db_storage = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    db_power_unit = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    db_cooling = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    db_case = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()

class ItemWidget(QWidget):

    def __init__(self, id_widget: int, parent=None, image=None, name=None):
        super(ItemWidget, self).__init__(parent)
        self.ui = Ui_item()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.widget.setTitle(str(id_widget))
        self.image = QPixmap(image)
        self.ui.label.setPixmap(self.image)
        self.ui.label_2.setText(name)
class ItemWidget2(QWidget):
    delete = pyqtSignal(int)

    def __init__(self, id_widget: int, parent=None, image=None, name=None):
        super(ItemWidget2, self).__init__(parent)
        self.ui = Ui_item2()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.widget.setTitle(str(id_widget))
        self.ui.btn_delete.clicked.connect(self.press_del)
        self.image = QPixmap(image)
        self.ui.label.setPixmap(self.image)
        self.ui.label_2.setText(name)

    @pyqtSlot()
    def press_del(self):
        self.delete.emit(self.id_widget)
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.counter_id: int = 0
        self.showFullScreen()
        self.ui.btn_exit.clicked.connect(exit)
        self.btn()

    def btn(self):
        self.ui.btn_CPU.clicked.connect(lambda: self.clear_area())
        self.ui.btn_CPU.clicked.connect(lambda: self.add_widget_CPU())

    def add(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_2.addWidget(item)
        item.delete.connect(self.delete_widget)
        print(id_widget)

    @pyqtSlot()
    def add_widget_CPU(self):
        self.counter_id = 0
        while self.counter_id != db_CPU[0][0]:
            self.counter_id += 1
            image = (image_CPU[self.counter_id - 1][0])
            name = (name_CPU[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add(id_widget, image, name))

    def add_widget_GPU(self):
        pass

    def add_widget_motherboard(self):
        pass

    def add_widget_RAM(self):
        pass

    def add_widget_storage_device(self):
        pass

    def add_widget_power_unit(self):
        pass

    def add_widget_cooling(self):
        pass

    def add_widget_case(self):
        pass

    @pyqtSlot()
    def clear_area(self):
        while self.ui.layout.count() > 0:
            item = self.ui.layout.takeAt(0)
            item.widget().deleteLater()

    @pyqtSlot(int)
    def delete_widget(self, wid: int):
        print(wid)
        widget = self.sender()
        self.ui.layout_2.removeWidget(widget)
        widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())