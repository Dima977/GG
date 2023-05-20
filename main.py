from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QScrollArea, QPushButton)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from mainwindow import Ui_MainWindow
from item import Ui_item
from item2 import Ui_item2
from configuration import Ui_configuration
import sqlite3
import sys

configuration = [0, 0, 0, 0, 0, 0, 0, 0]

with sqlite3.connect("PR.db") as db:
    cur = db.cursor()

    db_CPU = cur.execute("""select CPU_ID, image,name from CPU""").fetchall()

    db_GPU = cur.execute("""select GPU_ID, image, name from GPU""").fetchall()



    db_RAM = cur.execute("""select RAM_ID, image, name from RAM""").fetchall()

    db_power_unit = cur.execute("""select power_ID, image, name from power_unit""").fetchall()

    db_cooling = cur.execute("""select cooling_ID, image, name from cooling""").fetchall()

    db_case = cur.execute("""select case_ID, image, name from `case`""").fetchall()

    db_storage = cur.execute("""select storage_ID, image, name from storage_device""").fetchall()

class ConfigWidget(QWidget):

    def __init__(self, parent=None):
        super(ConfigWidget, self).__init__(parent)
        self.ui = Ui_configuration()
        self.ui.setupUi(self)

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
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.pushButton.clicked.connect(self.con_show)

    def con_show(self):
        self.w = ConfigWidget()
        self.w.show()

    def btn(self):
        self.ui.btn_CPU.clicked.connect(lambda: self.clear_area())
        self.ui.btn_CPU.clicked.connect(lambda: self.widget_CPU())

        self.ui.btn_GPU.clicked.connect(lambda: self.clear_area())
        self.ui.btn_GPU.clicked.connect(lambda: self.widget_GPU())

        self.ui.btn_motherboard.clicked.connect(lambda: self.clear_area())
        self.ui.btn_motherboard.clicked.connect(lambda: self.widget_motherboard())

        self.ui.btn_RAM.clicked.connect(lambda: self.clear_area())
        self.ui.btn_RAM.clicked.connect(lambda: self.widget_RAM())

        self.ui.btn_power_unit.clicked.connect(lambda: self.clear_area())
        self.ui.btn_power_unit.clicked.connect(lambda: self.widget_power_unit())

        self.ui.btn_cooling.clicked.connect(lambda: self.clear_area())
        self.ui.btn_cooling.clicked.connect(lambda: self.widget_cooling())

        self.ui.btn_case.clicked.connect(lambda: self.clear_area())
        self.ui.btn_case.clicked.connect(lambda: self.widget_case())

        self.ui.btn_storage_device.clicked.connect(lambda: self.clear_area())
        self.ui.btn_storage_device.clicked.connect(lambda: self.widget_storage_device())

    def add_CPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_CPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[0] = id_widget
        if self.ui.layout_CPU.count() > 0:
            self.ui.btn_motherboard.setEnabled(True)
        else:
            self.ui.btn_motherboard.setEnabled(False)
        with sqlite3.connect("PR.db") as db:

            cur = db.cursor()

        self.db_motherboard = cur.execute(f"""SELECT motherboard_ID, image, name
        FROM motherboard
        WHERE socket = (
          SELECT socket
          FROM CPU
          WHERE CPU_ID = {configuration[0]})""").fetchall()

    def add_GPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_GPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[1] = id_widget

    def add_motherboard(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_motherboard.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[2] = id_widget

    def add_RAM(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_RAM.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[3] = id_widget

    def add_power_unit(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_power_unit.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[5] = id_widget

    def add_cooling(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_cooling.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[6] = id_widget

    def add_case(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_case.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[7] = id_widget

    def add_storage_device(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_storage_device.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[4] = id_widget

    @pyqtSlot()
    def widget_CPU(self):
        self.counter_id = 0
        for i in db_CPU:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_CPU())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_CPU(id_widget, image, name))

    def widget_GPU(self):
        self.counter_id = 0
        for i in db_GPU:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_GPU())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_GPU(id_widget, image, name))

    def widget_motherboard(self):
        self.counter_id = 0
        for i in self.db_motherboard:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_motherboard())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_motherboard(id_widget, image, name))

    def widget_RAM(self):
        self.counter_id = 0
        for i in db_RAM:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_RAM())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_RAM(id_widget, image,name))

    def widget_power_unit(self):
        self.counter_id = 0
        for i in db_power_unit:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_power_unit())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_power_unit(id_widget, image,name))

    def widget_cooling(self):
        self.counter_id = 0
        for i in db_cooling:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_cooling())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_cooling(id_widget, image,name))

    def widget_case(self):
        self.counter_id = 0
        for i in db_case:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_case())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_case(id_widget, image,name))

    def widget_storage_device(self):
        self.counter_id = 0
        for i in db_storage:
            self.counter_id += 1
            image = (i[1])
            name = (i[2])
            widget = ItemWidget(self.counter_id, image=image, name=name)
            self.ui.layout.addWidget(widget)
            widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_device())
            widget.ui.btn_add.clicked.connect(
                lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_device(id_widget, image,name))

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

    def clear_storage_device(self):
        while self.ui.layout_storage_device.count() > 0:
            item = self.ui.layout_storage_device.takeAt(0)
            item.widget().deleteLater()

    @pyqtSlot()
    def clear_area(self):
        while self.ui.layout.count() > 0:
            item = self.ui.layout.takeAt(0)
            item.widget().deleteLater()
    def clear_all(self):
        self.clear_CPU()
        self.clear_GPU()
        self.clear_motherboard()
        self.clear_RAM()
        self.clear_storage_device()
        self.clear_power_unit()
        self.clear_cooling()
        self.clear_case()

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