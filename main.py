from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QScrollArea, QPushButton)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from mainwindow import Ui_MainWindow
from item import Ui_item
from item2 import Ui_item2
import sqlite3
import sys

goods = [0, 0, 0, 0, 0, 0]

with sqlite3.connect("PR.db") as db:
    cur = db.cursor()

    db_CPU = cur.execute("""select count(CPU_ID) from CPU""").fetchall()
    image_CPU = cur.execute("""select image from CPU""").fetchall()
    name_CPU = cur.execute("""select name from CPU""").fetchall()

    db_GPU = cur.execute("""select count(GPU_ID) from GPU""").fetchall()
    image_GPU = cur.execute("""select image from GPU""").fetchall()
    name_GPU = cur.execute("""select name from GPU""").fetchall()

    db_motherboard = cur.execute("""select count(motherboard_ID) from motherboard""").fetchall()
    image_motherboard = cur.execute("""select image from motherboard""").fetchall()
    name_motherboard = cur.execute("""select name from motherboard""").fetchall()

    db_RAM = cur.execute("""select count(RAM_ID) from RAM""").fetchall()
    image_RAM = cur.execute("""select image from RAM""").fetchall()
    name_RAM = cur.execute("""select name from RAM""").fetchall()

    db_storage = cur.execute("""select count(storage_ID) from storage_device""").fetchall()
    image_storage = cur.execute("""select image from storage_device""").fetchall()
    name_storage = cur.execute("""select name from storage_device""").fetchall()

    db_power_unit = cur.execute("""select count(power_ID) from power_unit""").fetchall()
    image_power_unit = cur.execute("""select image from power_unit""").fetchall()
    name_power_unit = cur.execute("""select name from power_unit""").fetchall()

    db_cooling = cur.execute("""select count(cooling_ID) from cooling""").fetchall()
    image_cooling = cur.execute("""select image from cooling""").fetchall()
    name_cooling = cur.execute("""select name from cooling""").fetchall()

    db_case = cur.execute("""select count(case_ID) from `case`""").fetchall()
    image_case = cur.execute("""select image from `case`""").fetchall()
    name_case = cur.execute("""select name from `case`""").fetchall()


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
        self.ui.pushButton.clicked.connect(self.clear_all)

    def btn(self):
        self.ui.btn_CPU.clicked.connect(lambda: self.clear_area())
        self.ui.btn_CPU.clicked.connect(lambda: self.widget_CPU())

        self.ui.btn_GPU.clicked.connect(lambda: self.clear_area())
        self.ui.btn_GPU.clicked.connect(lambda: self.widget_GPU())

        self.ui.btn_motherboard.clicked.connect(lambda: self.clear_area())
        self.ui.btn_motherboard.clicked.connect(lambda: self.widget_motherboard())

        self.ui.btn_RAM.clicked.connect(lambda: self.clear_area())
        self.ui.btn_RAM.clicked.connect(lambda: self.widget_RAM())

        self.ui.btn_storage_device.clicked.connect(lambda: self.clear_area())
        self.ui.btn_storage_device.clicked.connect(lambda: self.widget_storage_device())

        self.ui.btn_power_unit.clicked.connect(lambda: self.clear_area())
        self.ui.btn_power_unit.clicked.connect(lambda: self.widget_power_unit())

        self.ui.btn_cooling.clicked.connect(lambda: self.clear_area())
        self.ui.btn_cooling.clicked.connect(lambda: self.widget_cooling())

        self.ui.btn_case.clicked.connect(lambda: self.clear_area())
        self.ui.btn_case.clicked.connect(lambda: self.widget_case())

    def add_CPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_CPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[0] = id_widget
        print(goods)

    def add_GPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_GPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    def add_motherboard(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_motherboard.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[2] = id_widget

    def add_RAM(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_RAM.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    def add_storage_device(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_storage_device.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    def add_power_unit(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_power_unit.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    def add_cooling(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_cooling.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    def add_case(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_case.addWidget(item)
        item.delete.connect(self.delete_widget)
        goods[1] = id_widget

    @pyqtSlot()
    def widget_CPU(self):
        self.counter_id = 0
        while self.counter_id != db_CPU[0][0]:
            self.counter_id += 1
            image = (image_CPU[self.counter_id - 1][0])
            name = (name_CPU[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_CPU())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_CPU(id_widget, image, name))

    def widget_GPU(self):
        self.counter_id = 0
        while self.counter_id != db_GPU[0][0]:
            self.counter_id += 1
            image = (image_GPU[self.counter_id - 1][0])
            name = (name_GPU[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_GPU())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_GPU(id_widget, image, name))

    def widget_motherboard(self):
        self.counter_id = 0
        while self.counter_id != db_motherboard[0][0]:
            self.counter_id += 1
            image = (image_motherboard[self.counter_id - 1][0])
            name = (name_motherboard[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_motherboard())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_motherboard(id_widget, image, name))

    def widget_RAM(self):
        self.counter_id = 0
        while self.counter_id != db_RAM[0][0]:
            self.counter_id += 1
            image = (image_RAM[self.counter_id - 1][0])
            name = (name_RAM[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_RAM())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_RAM(id_widget, image,name))
    def widget_storage_device(self):
        self.counter_id = 0
        while self.counter_id != db_storage[0][0]:
            self.counter_id += 1
            image = (image_storage[self.counter_id - 1][0])
            name = (name_storage[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_device())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_device(id_widget, image,name))

    def widget_power_unit(self):
        self.counter_id = 0
        while self.counter_id != db_power_unit[0][0]:
            self.counter_id += 1
            image = (image_power_unit[self.counter_id - 1][0])
            name = (name_power_unit[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_power_unit())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_power_unit(id_widget, image,name))

    def widget_cooling(self):
        self.counter_id = 0
        while self.counter_id != db_cooling[0][0]:
            self.counter_id += 1
            image = (image_cooling[self.counter_id - 1][0])
            name = (name_cooling[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_cooling())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_cooling(id_widget, image,name))

    def widget_case(self):
        self.counter_id = 0
        while self.counter_id != db_case[0][0]:
            self.counter_id += 1
            image = (image_case[self.counter_id - 1][0])
            name = (name_case[self.counter_id - 1][0])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_case())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_case(id_widget, image,name))

    def clear_CPU(self):
        while self.ui.layout_CPU.count() > 0:
            item = self.ui.layout_CPU.takeAt(0)
            item.widget().deleteLater()

    def clear_GPU(self):
        while self.ui.layout_GPU.count() > 0:
            item = self.ui.layout_GPU.takeAt(0)
            item.widget().deleteLater()

    def clear_motherboard(self):
        while self.ui.layout_motherboard.count() > 0:
            item = self.ui.layout_motherboard.takeAt(0)
            item.widget().deleteLater()

    def clear_RAM(self):
        while self.ui.layout_RAM.count() > 0:
            item = self.ui.layout_RAM.takeAt(0)
            item.widget().deleteLater()

    def clear_storage_device(self):
        while self.ui.layout_storage_device.count() > 0:
            item = self.ui.layout_storage_device.takeAt(0)
            item.widget().deleteLater()

    def clear_power_unit(self):
        while self.ui.layout_power_unit.count() > 0:
            item = self.ui.layout_power_unit.takeAt(0)
            item.widget().deleteLater()

    def clear_cooling(self):
        while self.ui.layout_cooling.count() > 0:
            item = self.ui.layout_cooling.takeAt(0)
            item.widget().deleteLater()

    def clear_case(self):
        while self.ui.layout_case.count() > 0:
            item = self.ui.layout_case.takeAt(0)
            item.widget().deleteLater()

    @pyqtSlot()
    def clear_area(self):
        while self.ui.layout.count() > 0:
            item = self.ui.layout.takeAt(0)
            item.widget().deleteLater()

    def clear_all(self):
        self.clear_CPU()
        self.clear_GPU()

    @pyqtSlot(int)
    def delete_widget(self):
        widget = self.sender()
        self.ui.layout_2.removeWidget(widget)
        widget.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())