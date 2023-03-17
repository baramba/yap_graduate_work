import sys
from datetime import datetime

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QDateEdit, QComboBox
from PyQt6.QtWidgets import QPushButton

from model import DType


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # self.setMinimumSize(QSize(700, 800))
        self.setWindowTitle("Генератор промокодов")

        self.title_Label = QLabel(self)
        self.title_Label.setText('Название:')
        self.title_line = QLineEdit(self)

        self.description_Label = QLabel(self)
        self.description_Label.setText('Описание:')
        self.description_line = QLineEdit(self)

        self.expired_Label = QLabel(self)
        self.expired_Label.setText('Код действителен дней:')
        self.expired_line = QLineEdit(self)

        self.start_at_Label = QLabel(self)
        self.start_at_Label.setText('Код действителен с:')
        self.start_at_line = QDateEdit()
        date_str = datetime.now().__str__()
        qdate = QtCore.QDate.fromString(date_str.split()[0], "yyyy-MM-dd")
        self.start_at_line.setDisplayFormat("dd-MM-yyyy")
        self.start_at_line.setDate(qdate)
        self.start_at_line.show()

        self.activates_possible_Label = QLabel(self)
        self.activates_possible_Label.setText('Количество возможных активаций:')
        self.activates_possible_line = QLineEdit(self)

        self.discount_type_Label = QLabel(self)
        self.discount_type_Label.setText('Тип лояльности:')
        self.discount_type_line = QComboBox()
        self.discount_type_line.addItem(DType.DISCOUNT_PERCENT)
        self.discount_type_line.addItem(DType.DISCOUNT_FIX)
        self.discount_type_line.addItem(DType.PRICE_FIX)

        self.discount_amount_Label = QLabel(self)
        self.discount_amount_Label.setText('Размер скидки/фикса:')
        self.discount_amount_line = QLineEdit(self)

        self.minimal_amount_Label = QLabel(self)
        self.minimal_amount_Label.setText('Минимальная сумма чека для применения скидки:')
        self.minimal_amount_line = QLineEdit(self)

        self.product_id_Label = QLabel(self)
        self.product_id_Label.setText('Product id:')
        self.product_id_line = QLineEdit(self)

        self.path_Label = QLabel(self)
        self.path_Label.setText('Сохранить в:')
        self.path_line = QLineEdit(self)

        self.count_codes_Label = QLabel(self)
        self.count_codes_Label.setText('Количество кодов для генерации:')
        self.count_codes_line = QLineEdit(self)

        # Размер элементов
        self.product_id_line.resize(200, 32)
        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)

        # Расположение элементов
        box = QtWidgets.QGridLayout()
        box.addWidget(self.title_Label, 0, 1)
        box.addWidget(self.title_line, 0, 2)
        box.addWidget(self.description_Label, 1, 1)
        box.addWidget(self.description_line, 1, 2)
        box.addWidget(self.expired_Label, 2, 1)
        box.addWidget(self.expired_line, 2, 2)
        box.addWidget(self.start_at_Label, 3, 1)
        box.addWidget(self.start_at_line, 3, 2)
        box.addWidget(self.activates_possible_Label, 4, 1)
        box.addWidget(self.activates_possible_line, 4, 2)
        box.addWidget(self.discount_type_Label, 5, 1)
        box.addWidget(self.discount_type_line, 5, 2)
        box.addWidget(self.discount_amount_Label, 6, 1)
        box.addWidget(self.discount_amount_line, 6, 2)
        box.addWidget(self.minimal_amount_Label, 7, 1)
        box.addWidget(self.minimal_amount_line, 7, 2)
        box.addWidget(self.product_id_Label, 8, 1)
        box.addWidget(self.product_id_line, 8, 2)
        box.addWidget(self.path_Label, 9, 1)
        box.addWidget(self.path_line, 9, 2)
        box.addWidget(self.count_codes_Label, 10, 1)
        box.addWidget(self.count_codes_line, 10, 2)

        box.addWidget(pybutton, 11, 2)

        wdg = QtWidgets.QWidget()
        wdg.setLayout(box)
        self.setCentralWidget(wdg)

    def clickMethod(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
