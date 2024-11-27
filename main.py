import sys
import sqlite3
from random import randint
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class AddWidget(QMainWindow):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.conn = sqlite3.connect('coffee.sqlite')
        cur = self.conn.cursor()
        self.params = dict(cur.execute("""SELECT title, id FROM Types""").fetchall())
        self.current_param = self.params[list(self.params.keys())[0]]
        cur.close()

        self.comboBox.addItems(self.params.keys())

        self.coffee_id = coffee_id
        if coffee_id:
            result = self.conn.cursor().execute(f'''SELECT title, 
                                                          step_of_fire,
                                                          (SELECT title FROM Types WHERE id = type), 
                                                          describe,
                                                          cost,
                                                          V
                                                   FROM Information
                                                          WHERE id = ?''', (coffee_id,)).fetchone()
            self.plainTextEdit.setPlainText(result[0])
            self.plainTextEdit_2.setPlainText(result[1])
            self.comboBox.setCurrentText(result[2])
            self.plainTextEdit_5.setPlainText(result[3])
            self.plainTextEdit_3.setPlainText(str(result[4]))
            self.plainTextEdit_4.setPlainText(str(result[5]))
            self.pushButton.clicked.connect(self.update_coffee)
        else:
            self.pushButton.clicked.connect(self.create_coffee)

    def check(self):
        if self.plainTextEdit.toPlainText() and self.plainTextEdit_2.toPlainText() and self.plainTextEdit_5.toPlainText():
            a = self.plainTextEdit_3.toPlainText()
            b = self.plainTextEdit_4.toPlainText()
            if a.isdigit() and b.isdigit():
                return True
        return False

    def update_coffee(self):
        if self.check():
            self.conn.cursor().execute(f'''UPDATE Information SET title = '{self.plainTextEdit.toPlainText()}',
                                                              step_of_fire = '{self.plainTextEdit_2.toPlainText()}',
                                                              type = {self.params[self.comboBox.currentText()]},
                                                              describe = '{self.plainTextEdit_5.toPlainText()}',
                                                              cost = {self.plainTextEdit_3.toPlainText()},
                                                              V = {self.plainTextEdit_4.toPlainText()} WHERE id = {self.coffee_id}''')
            self.conn.commit()
            self.parent().update_coffees()
            self.close()
        self.statusBar().showMessage('Неверно заполнена форма')

    def create_coffee(self):
        if self.check():
            self.conn.cursor().execute(f'''INSERT INTO Information(title, step_of_fire, type, describe, cost, V)
                                                  VALUES('{self.plainTextEdit.toPlainText()}',
                                                          '{self.plainTextEdit_2.toPlainText()}',
                                                          {self.params[self.comboBox.currentText()]},
                                                          '{self.plainTextEdit_5.toPlainText()}',
                                                          {self.plainTextEdit_3.toPlainText()},
                                                          {self.plainTextEdit_4.toPlainText()})''')
            self.conn.commit()
            self.parent().update_coffees()
            self.close()
        self.statusBar().showMessage('Неверно заполнена форма')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.conn = sqlite3.connect('coffee.sqlite')
        self.update_coffees()

        self.pushButton.clicked.connect(self.add_coffee)
        self.pushButton_2.clicked.connect(self.edit_coffee)
        self.pushButton_3.clicked.connect(self.delete_coffee)
    
    def add_coffee(self):
        self.add_coffee_widget = AddWidget(self)
        self.add_coffee_widget.show()

    def edit_coffee(self):
        ids = self.selected_ids(self.tableWidget)
        if len(ids) == 1:
            self.edit_coffee_widget = AddWidget(self, ids[0])
            self.edit_coffee_widget.show()
            return
        self.statusBar().showMessage('Ничего не выбрано')

    def update_coffees(self):
        cur = self.conn.cursor()
        result = cur.execute('''SELECT * FROM Information''').fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'title', 'step_of_fire', 'type', 'describe', 'cost', 'V'])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def delete_coffee(self):
        ids = self.selected_ids(self.tableWidget)
        if not ids:
            self.statusBar().showMessage('Ничего не выбрано')
            return
        valid = QMessageBox.question(self, '',
                                     "Действительно заменить элементы с "
                                     "id " + ",".join(ids),
                                     buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if valid == QMessageBox.StandardButton.Yes:
            cursor = self.conn.cursor()
            for i in ids:
                cursor.execute('''DELETE FROM Information
                WHERE id = ?''', (int(i),))
            self.conn.commit()
            self.update_coffees()
    
    def selected_ids(self, table):
        rows = list(set([i.row() for i in table.selectedItems()]))
        ids = [table.item(i, 0).text() for i in rows]
        return ids


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())