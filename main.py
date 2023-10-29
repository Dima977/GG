from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QScrollArea, QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from reportlab.platypus import SimpleDocTemplate
from mainwindow import Ui_MainWindow
from item import Ui_item
from item2 import Ui_item2
from configuration import Ui_configuration
from customWidget import Ui_CustomWidget
import sqlite3
import datetime
import sys
from sites_parsers import parser_hardprice, parser_n_katalog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os

configuration = [0, 0, 0, 0, 0, 0, 0, 0]

with sqlite3.connect("configurator_v1.db") as db:
    cur = db.cursor()

    db_CPU = cur.execute("""select image, name, shops from cpu""").fetchall()

    db_GPU = cur.execute("""select image, name, shops from GPU""").fetchall()

    db_power_unit = cur.execute("""select image, name, shops from power_supply_units""").fetchall()

    db_cooling = cur.execute("""select image, name, shops from cooling""").fetchall()

    db_case = cur.execute("""select image, name, shops from cases""").fetchall()

DB_NAME = 'configurator_v1.db'
TODAY = datetime.date.today().strftime("%d-%m-%y")

def selectExecute(req):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(req)
    data = cur.fetchall()
    conn.close()
    return data

def shopsListToDBString(shops):
    str_shops = ''
    for shop in shops:
        str_shops += (str(shop)
                      .replace('[[', '')
                      .replace(']]', ';')
                      .replace('[', '')
                      .replace(']', ';')
                      .replace(' ', '')
                      .replace('\'', ''))
    return str_shops

class CustomWidget(QWidget):

    def __init__(self, id_widget: int, parent=None, image=None, name=None):
        super(CustomWidget, self).__init__(parent)
        self.ui = Ui_CustomWidget()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.widget.setTitle(str(id_widget))
        self.image = QPixmap(image)
        self.ui.label.setPixmap(self.image)
        self.ui.label_2.setText(name)

class ConfigWidget(QWidget):

    def __init__(self):
        super(ConfigWidget, self).__init__()
        self.ui = Ui_configuration()
        self.ui.setupUi(self)

class ItemWidget(QWidget):

    def __init__(self, id_widget: int, parent=None, image=None, name=None, shop=None):
        super(ItemWidget, self).__init__(parent)
        self.ui = Ui_item()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.widget.setTitle(str(id_widget))
        self.image = QPixmap(image)
        self.ui.label.setPixmap(self.image)
        self.ui.label_2.setText(name)
        self.ui.label_price.setText('Ценовой диапазон: ' + shop)
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

        self.ui.btn_storage_m2.clicked.connect(lambda: self.clear_area())
        self.ui.btn_storage_m2.clicked.connect(lambda: self.widget_storage_m2())

        self.ui.btn_storage_sata.clicked.connect(lambda: self.clear_area())
        self.ui.btn_storage_sata.clicked.connect(lambda: self.widget_storage_sata())

    def start(self, name):  # start button
        data = selectExecute(f'SELECT date, shops FROM {self.category} WHERE name="{name}";')[0]
        shops = data[1].split(';')
        if shops[-1] == '' and len(shops) > 1:
            shops.pop()
        if data[0] != TODAY or len(shops) <= 1:
            self.startParsing(name, shops)
        else:
            self.showHardwareInfCached(name)

    def startParsing(self, name, shopsStringsDB):
        n_katalog_str = ''
        for shop in shopsStringsDB:
            if 'n-katalog' in shop:
                n_katalog_str = shop + ";"
                break
        shops = parser_n_katalog.parse(n_katalog_str)
        if len(shops) == 0:
            shops = parser_hardprice.parse(name)
        self.showHardwareInf(name, shops)
        if len(shops) >= 1:
            shops.insert(0, n_katalog_str)
            str_shops = shopsListToDBString(shops)
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            update_execute = f'UPDATE {self.category} SET date = "{TODAY}", shops = "{str_shops}" WHERE name = "{name}";'
            try:
                cur.execute(update_execute)
                conn.commit()
            except Exception as exception:
                print(exception)
            finally:
                conn.close()
            with open('log.txt', 'a') as log_file:
                log_file.write(update_execute + '\n')
        else:
            print('Данные не обновлены, len(shops)<=1')

    def getHardwareInfDB(self, name, req_shops=False):
        inf = []
        shops_str = ''
        if req_shops:
            shops_str = 'shops, '
        if self.category == 'cpu':
            inf = selectExecute(f'SELECT {shops_str}image, cores, socket, ram_types FROM cpu WHERE name="{name}";')[0]
        elif self.category == 'gpu':
            inf = selectExecute(f'SELECT {shops_str}image FROM gpu WHERE name="{name}";')[0]
        elif self.category == 'ram':
            inf = \
            selectExecute(f'SELECT {shops_str}image, type, count, memory, frequency FROM ram WHERE name="{name}";')[0]
        elif self.category == 'motherboards':
            inf = selectExecute(
                f'SELECT {shops_str}image, socket, memory_count, ram_type, SATA_count, m2_count, pci_e_version, pci_e_x16_count, pci_e_x1_count FROM motherboards WHERE name="{name}";')[
                0]
        elif self.category == 'power_supply_units':
            inf = selectExecute(f'SELECT {shops_str}image, power FROM power_supply_units WHERE name="{name}";')[0]
        elif self.category == 'drives':
            inf = selectExecute(f'SELECT {shops_str}image, size, interface, type FROM drives WHERE name="{name}";')[0]
        elif self.category == 'cooling':
            inf = selectExecute(f'SELECT {shops_str}image, sockets FROM cooling WHERE name="{name}";')[0]
        elif self.category == 'cases':
            inf = selectExecute(f'SELECT shops, image, coolers_count FROM cases WHERE name="{name}";')[0]
        return inf

    def showHardwareInfCached(self, name):
        inf = self.getHardwareInfDB(name, True)
        shops = inf[0].split(';')
        if shops[-1] == '' and len(shops) > 1:
            shops.pop()
        for shop in shops:
            print(shop)
        for i in range(1, len(inf)):
            print(inf[i])

    def showHardwareInf(self, name, shops):
        print(name)
        print(self.category)
        inf = self.getHardwareInfDB(name, False)
        for shop in shops:
            print(shop)
        for inf in inf:
            print(inf)

    def add_CPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_CPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[0] = id_widget
        self.selection_motherboard()

    def selection_motherboard(self):
        if self.ui.layout_CPU.count() > 0:
            self.ui.btn_motherboard.setEnabled(True)
        else:
            self.ui.btn_motherboard.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_motherboard = cur.execute(f"""SELECT image, name, shops
        FROM motherboards
        WHERE socket = (
          SELECT socket
          FROM cpu
          WHERE ID = {configuration[0]})""").fetchall()

    def add_GPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_GPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[1] = id_widget

    def add_motherboard(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_motherboard.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[2] = id_widget
        self.selection_ram()
        self.selection_motherboard()
        self.selection_m2()
        self.selection_SATA()

    def add_RAM(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.ui.layout_RAM.addWidget(item)
        self.ram_count = item.ui.spin_box.value()
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_ram = cur.execute(f"""SELECT memory_count FROM motherboards""").fetchall()
        for i in db_count_ram:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        item.delete.connect(self.delete_widget)
        configuration[3] = id_widget

    def selection_ram(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_RAM.setEnabled(True)
        else:
            self.ui.btn_RAM.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_RAM = cur.execute(f"""SELECT  image, name, shops
                FROM ram
                WHERE type = (
                  SELECT ram_type
                  FROM motherboards
                  WHERE ID = {configuration[2]})""").fetchall()

    def add_power_unit(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_power_unit.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[5] = id_widget

    def add_cooling(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_cooling.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[6] = id_widget

    def add_case(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_case.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[7] = id_widget

    def add_storage_m2(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.m2_count = item.ui.spin_box.value()
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_m2 = cur.execute(f"""SELECT m2_count FROM motherboards""").fetchall()
        for i in db_count_m2:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        self.ui.layout_storage_m2.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[4] = id_widget

    def selection_m2(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_storage_m2.setEnabled(True)
        else:
            self.ui.btn_storage_m2.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_storage_m2 = cur.execute(f"""SELECT  image, name, shops FROM drives WHERE interface = "m2" """).fetchall()

    def add_storage_sata(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_SATA = cur.execute(f"""SELECT SATA_count FROM motherboards""").fetchall()
        for i in db_count_SATA:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        self.ui.layout_storage_SATA.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[4] = id_widget

    def selection_SATA(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_storage_sata.setEnabled(True)
        else:
            self.ui.btn_storage_sata.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_storage_SATA = cur.execute(f"""SELECT  image, name, shops FROM drives WHERE interface = "SATA" """).fetchall()

    def widget_CPU(self):
        self.category = 'cpu'
        self.counter_id = 0
        for i in db_CPU:
            self.counter_id += 1
            image = i[0]
            name = i[1]
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_CPU())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_CPU(id_widget, image, name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_GPU(self):
        self.category = 'gpu'
        self.counter_id = 0
        for i in db_GPU:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_GPU())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_GPU(id_widget, image, name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_motherboard(self):
        self.category = 'motherboards'
        self.counter_id = 0
        for i in self.db_motherboard:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_motherboard())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_motherboard(id_widget, image, name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_RAM(self):
        self.category = 'ram'
        self.counter_id = 0
        for i in self.db_RAM:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_RAM())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_RAM(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_power_unit(self):
        self.category = 'power_supply_units'
        self.counter_id = 0
        for i in db_power_unit:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_power_unit())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_power_unit(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_cooling(self):
        self.category = 'cooling'
        self.counter_id = 0
        for i in db_cooling:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_cooling())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_cooling(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_case(self):
        self.category = 'cases'
        self.counter_id = 0
        for i in db_case:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_case())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_case(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_storage_m2(self):
        self.category = 'drives'
        self.counter_id = 0
        for i in self.db_storage_m2:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_m2())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_m2(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

    def widget_storage_sata(self):
        self.category = 'drives'
        self.counter_id = 0
        for i in self.db_storage_SATA:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_sata())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_sata(id_widget, image,name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.showHardwareInfCached(name))

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

    def clear_storage_m2(self):
        while self.ui.layout_storage_m2.count() > 0:
            item = self.ui.layout_storage_m2.takeAt(0)
            item.widget().deleteLater()

    def clear_storage_sata(self):
        while self.ui.layout_storage_SATA.count() > 0:
            item = self.ui.layout_storage_SATA.takeAt(0)
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
        self.clear_storage_sata()
        self.clear_storage_m2()
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