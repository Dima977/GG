from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from item import Ui_item

class ItemWidget(QWidget):

    def __init__(self, id_widget: int, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.ui = Ui_item()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.widget.setTitle(str(id_widget))




