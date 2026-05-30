import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, \
    QDialog, QLabel, QLineEdit, QComboBox, QTextEdit, \
    QMessageBox, QTableWidget


class AddEditCoffeeDialog(QDialog):
    def __init__(self, parent=None, record_id=None):
        super().__init__(parent)
        self.record_id = record_id
        self.initUI()
        if record_id:
            self.load_record()
            self.setWindowTitle('Редактирование записи о кофе')
        else:
            self.setWindowTitle('Добавление новой записи о кофе')

    def initUI(self):
        self.setGeometry(400, 200, 500, 550)

        y_pos = 20

        if self.record_id:
            self.id_label = QLabel(f"ID записи: {self.record_id}", self)
            self.id_label.move(20, y_pos)
            y_pos += 30

        self.label_name = QLabel('Название сорта:', self)
        self.label_name.move(20, y_pos)
        self.name_edit = QLineEdit(self)
        self.name_edit.setGeometry(20, y_pos + 25, 460, 30)
        y_pos += 65

        self.label_roast = QLabel('Степень обжарки:', self)
        self.label_roast.move(20, y_pos)
        self.roast_combo = QComboBox(self)
        self.roast_combo.setGeometry(20, y_pos + 25, 460, 30)
        self.roast_combo.addItems(['Светлая', 'Средняя', 'Темная'])
        y_pos += 65

        self.label_grind = QLabel('Молотый/в зернах:', self)
        self.label_grind.move(20, y_pos)
        self.grind_combo = QComboBox(self)
        self.grind_combo.setGeometry(20, y_pos + 25, 460, 30)
        self.grind_combo.addItems(['В зернах', 'Молотый'])
        y_pos += 65

        self.label_taste = QLabel('Описание вкуса:', self)
        self.label_taste.move(20, y_pos)
        self.taste_text = QTextEdit(self)
        self.taste_text.setGeometry(20, y_pos + 25, 460, 100)
        y_pos += 135

        self.label_price = QLabel('Цена:', self)
        self.label_price.move(20, y_pos)
        self.price_edit = QLineEdit(self)
        self.price_edit.setGeometry(20, y_pos + 25, 460, 30)
        y_pos += 65

        self.label_weight = QLabel('Объем упаковки:', self)
        self.label_weight.move(20, y_pos)
        self.weight_edit = QLineEdit(self)
        self.weight_edit.setGeometry(20, y_pos + 25, 460, 30)
        y_pos += 65

        self.btn_save = QPushButton('Сохранить', self)
        self.btn_save.setGeometry(100, y_pos, 120, 35)
        self.btn_save.clicked.connect(self.save_record)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setGeometry(280, y_pos, 120, 35)
        self.btn_cancel.clicked.connect(self.reject)

    def load_record(self):
        try:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            res = cur.execute("""SELECT name, roast_level, grind_type, taste_description, price, package_weight 
                                       FROM coffee WHERE id = ?""", (self.record_id,)).fetchone()
            con.close()

            if res:
                self.name_edit.setText(res[0])
                self.roast_combo.setCurrentText(res[1])
                self.grind_combo.setCurrentText(res[2])
                self.taste_text.setText(res[3] if res[3] else '')
                self.price_edit.setText(str(res[4]))
                self.weight_edit.setText(str(res[5]))
            else:
                QMessageBox.warning(self, "Ошибка", "Запись не найдена!")
                self.reject()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить запись:\n{str(e)}")
            self.reject()

    def save_record(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Название сорта обязательно для заполнения!")
            return

        roast = self.roast_combo.currentText()
        grind = self.grind_combo.currentText()
        taste = self.taste_text.toPlainText().strip()
        if not taste:
            taste = None

        price_text = self.price_edit.text().strip()
        if not price_text:
            QMessageBox.warning(self, "Ошибка", "Поле 'Цена' обязательно для заполнения!")
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Поле 'Цена' должно содержать число!")
            return

        weight = self.weight_edit.text().strip()
        if not weight:
            QMessageBox.warning(self, "Ошибка", "Поле 'Объем упаковки' обязательно для заполнения!")
            return
        try:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()

            if self.record_id:
                cur.execute("""
                            UPDATE coffee 
                            SET name=?, roast_level=?, grind_type=?, taste_description=?, price=?, package_weight=?
                            WHERE id=?
                        """, (name, roast, grind, taste, price, weight, self.record_id))
            else:
                cur.execute("""
                            INSERT INTO coffee (name, roast_level, grind_type, taste_description, price, package_weight)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (name, roast, grind, taste, price, weight))

            con.commit()
            con.close()
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось сохранить запись:\n{str(e)}")

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setGeometry(300, 300, 1100, 600)
        self.setWindowTitle('Информация о кофе')

        self.btn_add = QPushButton('Добавить запись', self)
        self.btn_add.resize(150, 30)
        self.btn_add.move(20, 20)
        self.btn_add.clicked.connect(self.add_record)

        self.btn_edit = QPushButton('Редактировать запись', self)
        self.btn_edit.resize(150, 30)
        self.btn_edit.move(180, 20)
        self.btn_edit.clicked.connect(self.edit_record)

        self.btn_refresh = QPushButton('Обновить', self)
        self.btn_refresh.resize(150, 30)
        self.btn_refresh.move(340, 20)
        self.btn_refresh.clicked.connect(self.load_data)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(1060, 500)
        self.tableWidget.move(20, 60)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def load_data(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("""SELECT id, name, roast_level, grind_type, taste_description, price, package_weight 
                           FROM coffee ORDER BY id""").fetchall()
        con.close()

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
             'Описание вкуса', 'Цена', 'Объем упаковки']
        )

        for row, line in enumerate(res):
            for col, value in enumerate(line):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def add_record(self):
        dialog = AddEditCoffeeDialog(self)
        if dialog.exec():
            self.load_data()

    def edit_record(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            return

        record_id = int(self.tableWidget.item(selected_row, 0).text())
        dialog = AddEditCoffeeDialog(self, record_id)
        if dialog.exec():
            self.load_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())