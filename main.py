import sys
import sqlite3
from random import randint
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.do_paint = False
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.conn = sqlite3.connect('coffee.sqlite')
        cur = self.conn.cursor()
        result = cur.execute('''SELECT * FROM Information''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'title', 'step_of_fire', 'type', 'description', 'cost', 'V'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())