import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle('Информация о кофе')

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(960, 450)
        self.tableWidget.move(20, 20)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def load_data(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        res = cur.execute("""SELECT id, name, roast_level, grind_type, taste_description, price, package_weight 
                           FROM coffee""").fetchall()
        con.close()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
             'Описание вкуса', 'Цена', 'Объем упаковки']
        )

        for row, line in enumerate(res):
            for col, value in enumerate(line):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeApp()
    ex.show()
    sys.exit(app.exec())