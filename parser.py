import datetime
import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from sites_parsers import parser_hardprice, parser_n_katalog
from gui_test import Ui_MainWindow

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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.comboBox.addItems(['cpu', 'gpu', 'ram', 'motherboards', 'power_supply_units', 'drives', 'cooling', 'cases'])
        self.comboBox.currentIndexChanged.connect(self.getHardwareTableFromDB)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['name', 'цена'])
        self.tableWidget.setColumnWidth(1, 300)
        self.getHardwareTableFromDB()


    def printHardwareFromDB(self):
        rowsDB = selectExecute(f'SELECT name, shops FROM {self.comboBox.currentText()};')
        for row_i in range(len(rowsDB)):
            print('name:', str(rowsDB[row_i][0]))
            shops = rowsDB[row_i][1].split(';')
            for shop in shops:
                if 'n-katalog' in shop:
                    print('Ценовой диапазон: ' + shop.split(',')[2])
                    break


    def getHardwareTableFromDB(self):
        rowsDB = selectExecute(f'SELECT name, shops FROM {self.comboBox.currentText()};')
        self.tableWidget.setRowCount(len(rowsDB))
        for row_i in range(len(rowsDB)):
            self.tableWidget.setItem(row_i, 0, QTableWidgetItem(str(rowsDB[row_i][0])))  # name
            shops = rowsDB[row_i][1].split(';')
            for shop in shops:
                if 'n-katalog' in shop:
                    self.tableWidget.setItem(row_i, 1, QTableWidgetItem('Ценовой диапазон: ' + shop.split(',')[2]))
                    break

    def start(self):  # start button
        name = self.tableWidget.selectedIndexes()[0].data()
        data = selectExecute(f'SELECT date, shops FROM {self.comboBox.currentText()} WHERE name="{name}";')[0]
        shops = data[1].split(';')
        if shops[-1] == '' and len(shops) > 1:
            shops.pop()  # удаление пустого элемента после разбиения строки через ;
        if data[0] != TODAY or len(shops)<=1:
            self.startParsing(name, shops)
        else:
            self.showHardwareInfCached(name)

    def startParsing(self, name, shopsStringsDB):
        # получение строки данных n_katalog из списка shops базы
        n_katalog_str = ''
        for shop in shopsStringsDB:
            if 'n-katalog' in shop:
                n_katalog_str = shop + ";"
                break
        shops = parser_n_katalog.parse(n_katalog_str)  # 1 site parsing  #todo Swap 1-2
        if len(shops) == 0:
            shops = parser_hardprice.parse(name)  # 2 site parsing (reserve)
        self.showHardwareInf(name, shops)  # вывод информации о железе, без n-katalog
        # обновление БД
        if len(shops) >= 1:
            shops.insert(0, n_katalog_str)  # добавление n-katalog к строке для БД
            str_shops = shopsListToDBString(shops)
            # запись даты и данных магазинов в БД
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            update_execute = f'UPDATE {self.comboBox.currentText()} SET date = "{TODAY}", shops = "{str_shops}" WHERE name = "{name}";'
            try:
                cur.execute(update_execute)
                conn.commit()
            except Exception as exception: print(exception)  #
            finally: conn.close()
            # log
            with open('log.txt', 'a') as log_file:
                log_file.write(update_execute + '\n')
        else:
            print('Данные не обновлены, len(shops)<=1')  # log


    def getHardwareInfDB(self,name, req_shops = False):
        inf = []
        shops_str = ''
        if req_shops:
            shops_str = 'shops, '
        if self.comboBox.currentText()=='cpu':
            inf = selectExecute(f'SELECT {shops_str}image, cores, socket, ram_types FROM cpu WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='gpu':
            inf = selectExecute(f'SELECT {shops_str}image, FROM gpu WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='ram':
            inf = selectExecute(f'SELECT {shops_str}image, type, count, memory, frequency FROM ram WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='motherboards':
            inf = selectExecute(f'SELECT {shops_str}image, socket, memory_count, ram_type, SATA_count, m2_count, pci_e_version, pci_e_x16_count, pci_e_x1_count FROM motherboards WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='power_supply_units':
            inf = selectExecute(f'SELECT {shops_str}image, power FROM power_supply_units WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='drives':
            inf = selectExecute(f'SELECT {shops_str}image, size, interface, type FROM drives WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='cooling':
            inf = selectExecute(f'SELECT {shops_str}image, sockets FROM cooling WHERE name="{name}";')[0]
        elif self.comboBox.currentText()=='cases':
            inf = selectExecute(f'SELECT shops, image, coolers_count FROM cases WHERE name="{name}";')[0]
        return inf

    def showHardwareInfCached(self, name):
        print(name)
        print(self.comboBox.currentText())
        inf = self.getHardwareInfDB(name, True)
        shops = inf[0].split(';')
        if shops[-1] == '' and len(shops) > 1:
            shops.pop()
        for shop in shops:
            print(shop)
        for i in range(1, len(inf)):
            print(inf[i])

    def showHardwareInf(self,name, shops):
        print(name)
        print(self.comboBox.currentText())
        inf = self.getHardwareInfDB(name, False)
        for shop in shops:
            print(shop)
        for inf in inf:
            print(inf)

def application():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
