import logging
import sys
from datetime import timedelta

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from core.interface_gui import MainWindow
from core.main_script import local_script

from model import DataParam

log = logging.getLogger(__name__)


class Window(MainWindow):
    def clickMethod(self):
        try:
            data = DataParam(
                title=self.title_line.text(),
                description=self.description_line.text(),
                start_at=self.start_at_line.dateTime().toPyDateTime(),
                expired=(self.start_at_line.dateTime().toPyDateTime() + timedelta(days=int(self.expired_line.text()))),
                activates_possible=int(self.activates_possible_line.text()),
                discount_type=self.discount_type_line.currentText(),
                discount_amount=int(self.discount_amount_line.text()),
                minimal_amount=int(self.minimal_amount_line.text()),
                product_id=[self.product_id_line.text()] if self.product_id_line.text() != '' else None,
                path=f'./{self.path_line.text()}',
                count_codes=int(self.count_codes_line.text())
            )
            log.info("Data : %s" % data)
            local_script(data)
            log.info("finish")

        except Exception as e:
            log.error("Error %s" %e.__str__())
            msg = QMessageBox(text="Error", parent=self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.setInformativeText("Ошибка введенных данных \n \n" + e.__str__())
            msg.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec())
