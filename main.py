from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QScrollArea, QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from mainwindow import Ui_MainWindow
from item import Ui_item
from item2 import Ui_item2
from configuration import Ui_configuration
from customWidget import Ui_CustomWidget
import sqlite3
import datetime
import sys
from sites_parsers import parser_hardprice, parser_n_katalog
import create_pdf
from Spravkad import ComputerComponentsWindow

configuration = [0, 0, 0, 0, 0, 0, 0, 0, 0]
prices = ['', '', '', '', '', '', '', '', '']
test_names = ['', '', '', '', '', '', '', '', '']
test_tables = ['', '', '', '', '', '', '', '', '']

with sqlite3.connect("configurator_v1.db") as db:
    cur = db.cursor()

    db_CPU = cur.execute("""select image, name, shops, socket, cores, ram_types from cpu""").fetchall()

    db_GPU = cur.execute("""select image, name, shops  from GPU""").fetchall()

    db_power_unit = cur.execute("""select image, name, shops, power from power_supply_units""").fetchall()

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
class Spravka(QMainWindow):
    def __init__(self):
        super(Spravka, self).__init__()
        self.ui = Ui_configuration()
        self.ui.setupUi(self)


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
        self.ui.btn_help.clicked.connect(lambda: self.spravkashow())

        self.ui.pushButton.clicked.connect(lambda: self.toPdf())

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

    def spravkashow(self):
        self.spravka = ConfigWidget()
        self.spravka.show()

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

    def getHardwareInfDB(self, name, req_shops=False, table=None):
        inf = []
        shops_str = ''
        if req_shops:
            shops_str = 'shops, '
        if table is None:
            table = self.category
        if table == 'cpu':
            inf = selectExecute(f'SELECT {shops_str}image, cores, socket, ram_types FROM cpu WHERE name="{name}";')[0]
        elif table == 'gpu':
            inf = selectExecute(f'SELECT {shops_str}image FROM gpu WHERE name="{name}";')[0]
        elif table == 'ram':
            inf = \
                selectExecute(f'SELECT {shops_str}image, type, count, memory, frequency FROM ram WHERE name="{name}";')[
                    0]
        elif table == 'motherboards':
            inf = selectExecute(
                f'SELECT {shops_str}image, socket, memory_count, ram_type, SATA_count, m2_count, pci_e_version, pci_e_x16_count, pci_e_x1_count FROM motherboards WHERE name="{name}";')[
                0]
        elif table == 'power_supply_units':
            inf = selectExecute(f'SELECT {shops_str}image, power FROM power_supply_units WHERE name="{name}";')[0]
        elif table == 'drives':
            inf = selectExecute(f'SELECT {shops_str}image, size, interface, type FROM drives WHERE name="{name}";')[0]
        elif table == 'cooling':
            inf = selectExecute(f'SELECT {shops_str}image, sockets FROM cooling WHERE name="{name}";')[0]
        elif table == 'cases':
            inf = selectExecute(f'SELECT shops, image, coolers_count FROM cases WHERE name="{name}";')[0]
        return inf

    def showHardwareInfCached(self, name):
        pass
        # inf = self.getHardwareInfDB(name, True)
        # shops = inf[0].split(';')
        # if shops[-1] == '' and len(shops) > 1:
        #     shops.pop()
        # for shop in shops:
        #     print(shop)
        # for i in range(1, len(inf)):
        #     print(inf[i])

    def showHardwareInf(self, name, shops):
        pass
        # print(name)
        # print(self.category)
        # inf = self.getHardwareInfDB(name, False)
        # for shop in shops:
        #     print(shop)
        # for inf in inf:
        #     print(inf)

    def toPdf(self):
        names_list = []
        tables_list = []
        for i in range(len(test_names)):
            if test_names[i] != '':
                names_list.append(test_names[i])
                tables_list.append(test_tables[i])

        test_shops_tables = []
        for i in range(len(names_list)):
            inf = self.getHardwareInfDB(name=names_list[i], req_shops=True, table=tables_list[i])
            shops = []
            for shops_str in inf[0].split(';'):
                shops.append(shops_str.split(','))
            shops.pop(0)
            if shops[-1] == [''] and len(shops) > 1:
                shops.pop()
            test_shops_tables.append(shops)
        create_pdf.create(names_list, test_shops_tables)

    def getPrices(self, name, table):
        count = 1
        entry = self.getHardwareInfDB(name, True, table)
        shops = []
        for shops_str in entry[0].split(';'):
            shops.append(shops_str.split(','))
        shops.pop(0)
        if shops[-1] == [''] and len(shops) > 1:
            shops.pop()
        shops_prices = []
        for shop in shops:
            shops_prices.append(shop[2])
        return {'min': count * int(min(shops_prices)), 'max': count * int(max(shops_prices))}

    def fullPrice(self):
        min_sum = 0
        max_sum = 0
        for name in test_names:
            if name == '': continue
            a = self.getPrices(name, test_tables[test_names.index(name)])
            min_sum += a['min']
            max_sum += a['max']
        print(test_names)
        print(test_tables)
        self.ui.label_price.setText(str(min_sum) + '-' + str(max_sum))

    def add_CPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_CPU.addWidget(item)
        item.ui.btn_delete.clicked.connect(self.cl_cpu)
        item.ui.btn_delete.clicked.connect(lambda: self.clear_not_all())
        item.delete.connect(self.delete_widget)
        configuration[0] = id_widget
        self.selection_motherboard()
        self.fullPrice()

    def cl_cpu(self):
        test_tables[0] = ''
        test_names[0] = ''

    def selection_motherboard(self):
        if self.ui.layout_CPU.count() > 0:
            self.ui.btn_motherboard.setEnabled(True)
        else:
            self.ui.btn_motherboard.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_motherboard = cur.execute(f"""SELECT image, name, shops, socket, memory_count, ram_type, SATA_count, m2_count
        FROM motherboards
        WHERE socket = (
          SELECT socket
          FROM cpu
          WHERE ID = {configuration[0]})""").fetchall()

    def add_GPU(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_gpu)
        self.ui.layout_GPU.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[1] = id_widget
        self.fullPrice()

    def cl_gpu(self):
        test_tables[1] = ''
        test_names[1] = ''

    def add_motherboard(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_motherboards)
        self.ui.layout_motherboard.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[2] = id_widget
        self.selection_ram()
        self.selection_motherboard()
        self.selection_m2()
        self.selection_SATA()
        self.fullPrice()

    def cl_motherboards(self):
        test_tables[2] = ''
        test_names[2] = ''

    def add_RAM(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        self.ui.layout_RAM.addWidget(item)
        self.ram_count = item.ui.spin_box.valueChanged
        item.ui.btn_delete.clicked.connect(self.cl_ram)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_ram = cur.execute(f"""SELECT memory_count FROM motherboards""").fetchall()
        for i in db_count_ram:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        item.delete.connect(self.delete_widget)
        configuration[3] = id_widget
        self.fullPrice()

    def cl_ram(self):
        test_tables[3] = ''
        test_names[3] = ''

    def selection_ram(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_RAM.setEnabled(True)
        else:
            self.ui.btn_RAM.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_RAM = cur.execute(f"""SELECT  image, name, shops, type, frequency
                FROM ram
                WHERE type = (
                  SELECT ram_type
                  FROM motherboards
                  WHERE ID = {configuration[2]})""").fetchall()

    def add_power_unit(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_power)
        self.ui.layout_power_unit.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[4] = id_widget
        self.fullPrice()

    def cl_power(self):
        test_tables[4] = ''
        test_names[4] = ''

    def add_cooling(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_cooling)
        self.ui.layout_cooling.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[5] = id_widget
        self.fullPrice()

    def cl_cooling(self):
        test_tables[5] = ''
        test_names[5] = ''

    def add_case(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_case)
        self.ui.layout_case.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[6] = id_widget
        self.fullPrice()

    def cl_case(self):
        test_tables[6] = ''
        test_names[6] = ''

    def add_storage_m2(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        self.m2_count = item.ui.spin_box.value()
        item.ui.spin_box.hide()
        item.ui.btn_delete.clicked.connect(self.cl_m2)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_m2 = cur.execute(f"""SELECT m2_count FROM motherboards""").fetchall()
        for i in db_count_m2:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        self.ui.layout_storage_m2.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[7] = id_widget
        self.fullPrice()

    def cl_m2(self):
        test_tables[7] = ''
        test_names[7] = ''

    def selection_m2(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_storage_m2.setEnabled(True)
        else:
            self.ui.btn_storage_m2.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_storage_m2 = cur.execute(
            f"""SELECT  image, name, shops, size, type FROM drives WHERE interface = "m2" """).fetchall()

    def add_storage_sata(self, id_widget: int, image: str, name: str):
        item = ItemWidget2(id_widget, image=image, name=name)
        item.ui.btn_delete.clicked.connect(self.cl_sata)
        item.ui.spin_box.hide()
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        db_count_SATA = cur.execute(f"""SELECT SATA_count FROM motherboards""").fetchall()
        for i in db_count_SATA:
            item.ui.spin_box.setMaximum(i[0])
        item.ui.spin_box.setMinimum(1)
        self.ui.layout_storage_SATA.addWidget(item)
        item.delete.connect(self.delete_widget)
        configuration[8] = id_widget
        self.fullPrice()

    def cl_sata(self):
        test_tables[8] = ''
        test_names[8] = ''

    def selection_SATA(self):
        if self.ui.layout_motherboard.count() > 0:
            self.ui.btn_storage_sata.setEnabled(True)
        else:
            self.ui.btn_storage_sata.setEnabled(False)
        with sqlite3.connect("configurator_v1.db") as db:
            cur = db.cursor()
        self.db_storage_SATA = cur.execute(
            f"""SELECT  image, name, shops, size, type FROM drives WHERE interface = "SATA" """).fetchall()

    def widget_CPU(self):
        self.category = 'cpu'
        self.counter_id = 0
        for i in db_CPU:
            self.counter_id += 1
            image = i[0]
            name = i[1]
            shops = i[2].split(';')
            socket = i[3]
            cores = i[4]
            ram_types = i[5]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Сокет: {}\nКол-во ядер: {}\nТип памяти: {}\n".format(socket, cores, ram_types))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_CPU())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_cpu(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_CPU(id_widget, image,
                                                                                                     name))

    def qwe_cpu(self, name):
        test_tables[0] = 'cpu'
        test_names[0] = name
        self.showHardwareInfCached(name)

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
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_gpu(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_GPU(id_widget, image,
                                                                                                     name))
    def qwe_gpu(self, name):
        test_tables[1] = 'gpu'
        test_names[1] = name
        self.showHardwareInfCached(name)

    def widget_motherboard(self):
        self.category = 'motherboards'
        self.counter_id = 0
        for i in self.db_motherboard:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            socket = i[3]
            memory_count = i[4]
            ram_types = i[5]
            SATA_count = i[6]
            m2_count = i[7]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Сокет: {}\nКол-во памяти: {}\nТип памяти: {}\nКол-во M.2: {}\nКол-во SATA: {}\n".format(socket,
                                                                                                             memory_count,
                                                                                                             ram_types,
                                                                                                             SATA_count,
                                                                                                             m2_count))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_motherboard())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_motherboard(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_motherboard(id_widget,
                                                                                                             image,
                                                                                                             name))


    def qwe_motherboard(self, name):
        test_tables[2] = 'motherboards'
        test_names[2] = name
        self.showHardwareInfCached(name)

    def widget_RAM(self):
        self.category = 'ram'
        self.counter_id = 0
        for i in self.db_RAM:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            type = i[3]
            frequency = i[4]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Тип памяти: {}\nЧастота: {}\n".format(type, frequency))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_RAM())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_ram(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_RAM(id_widget, image,
                                                                                                     name))


    def qwe_ram(self, name):
        test_tables[3] = 'ram'
        test_names[3] = name
        self.showHardwareInfCached(name)

    def widget_power_unit(self):
        self.category = 'power_supply_units'
        self.counter_id = 0
        for i in db_power_unit:
            self.counter_id += 1
            image = i[0]
            name = i[1]
            shops = i[2].split(';')
            power = i[3]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Мощность: {}W\n".format(power))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_power_unit())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_power_unit(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_power_unit(id_widget,
                                                                                                            image,
                                                                                                            name))


    def qwe_power_unit(self, name):
        test_tables[4] = 'power_supply_units'
        test_names[4] = name
        self.showHardwareInfCached(name)

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
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_cooling(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_cooling(id_widget,
                                                                                                         image, name))


    def qwe_cooling(self, name):
        test_tables[5] = 'cooling'
        test_names[5] = name
        self.showHardwareInfCached(name)

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
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_case(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_case(id_widget, image,
                                                                                                      name))


    def qwe_case(self, name):
        test_tables[6] = 'cases'
        test_names[6] = name
        self.showHardwareInfCached(name)

    def widget_storage_m2(self):
        self.category = 'drives'
        self.counter_id = 0
        for i in self.db_storage_m2:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            size = i[3]
            type = i[4]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Размер памяти: {}\nТип: {}\n".format(size, type))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_m2())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_m2(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_m2(id_widget,
                                                                                                            image,
                                                                                                            name))

    def qwe_m2(self, name):
        test_tables[7] = 'drives'
        test_names[7] = name
        self.showHardwareInfCached(name)

    def widget_storage_sata(self):
        self.category = 'drives'
        self.counter_id = 0
        for i in self.db_storage_SATA:
            self.counter_id += 1
            image = (i[0])
            name = (i[1])
            shops = i[2].split(';')
            size = i[3]
            type = i[4]
            if 'n-katalog' in shops[0]:
                shop = shops[0].split(',')[2]
                widget = ItemWidget(self.counter_id, image=image, name=name, shop=shop)
                widget.ui.label_speki.setText(
                    "Размер памяти: {}\nТип: {}\n".format(size, type))
                self.ui.layout.addWidget(widget)
                widget.ui.btn_add.clicked.connect(lambda: self.clear_storage_sata())
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.start(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, name=name: self.qwe_sata(name))
                widget.ui.btn_add.clicked.connect(
                    lambda checked, id_widget=widget.id_widget, image=image, name=name: self.add_storage_sata(id_widget,
                                                                                                              image,
                                                                                                              name))


    def qwe_sata(self, name):
        test_tables[8] = 'drives'
        test_names[8] = name
        self.showHardwareInfCached(name)

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

    def clear_not_all(self):
        self.clear_motherboard()
        self.clear_RAM()
        self.clear_storage_sata()
        self.clear_storage_m2()
        self.clear_power_unit()
        self.clear_cooling()

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
