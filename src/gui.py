import sys
import json
from table import *
from PyQt5 import QtCore, QtWidgets, QtGui


class Gui(QtWidgets.QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.columns = 0
        self.rows = 0

        # сохранение
        save = QtWidgets.QAction(self)
        save.setShortcut('Ctrl+S')
        save.setText('Сохранить')
        save.triggered.connect(self.save)

        # открыть файл
        upload = QtWidgets.QAction(self)
        upload.setShortcut('Ctrl+O')
        upload.setText('Открыть')
        upload.triggered.connect(self.upload)
        # upload.setVisible(False)

        # добавить колонку
        add_column = QtWidgets.QAction(self)
        add_column.setShortcut('Ctrl+Shift+A')
        add_column.setText('Добавить колонку')
        add_column.triggered.connect(self.add_column)

        # добавить строку
        self.add_row = QtWidgets.QAction(self)
        self.add_row.setShortcut('Ctrl+Shift+R')
        self.add_row.setText('Добавить строку')
        self.add_row.triggered.connect(self.add_r)
        self.add_row.setVisible(False)

        self.ui.menu.addAction(add_column)
        self.ui.menu.addAction(self.add_row)
        self.ui.menu.addAction(save)
        self.ui.menu.addAction(upload)
        self.ui.pushButton.clicked.connect(self.clear_table)

    def add_column(self):
        self.columns += 1
        self.ui.tableWidget.setColumnCount(self.columns)
        if self.rows < 1:
            self.rows += 1
            self.ui.tableWidget.setRowCount(self.rows)
            self.add_row.setVisible(True)

    # добавить колонку
    def add_r(self):
        self.rows += 1
        self.ui.tableWidget.setRowCount(self.rows)

    # очистить таблицу
    def clear_table(self):
        self.ui.tableWidget.clear()

    def save(self):
        row_dict = {}
        row_list = []
        for column in range(self.ui.tableWidget.columnCount()):
            for row in range(self.ui.tableWidget.rowCount()):
                value = self.ui.tableWidget.item(row, column)
                if value is not None:
                    row_list.append(value.text())
                else: row_list.append('')
            row_dict[column] = row_list
            row_list = []
        with open('filename.json', 'w') as filename:
            json.dump(row_dict, filename, sort_keys=True, indent=4)

    def upload(self):
        column_count = 0
        column_name = []
        column = 0
        count = 0
        item = None
        # cell_data = []
        open_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')[0]
        with open(open_file) as file:
            data = json.load(file)
        for key in data.keys():
            column_count += 1
            column_name.append(key)
        self.ui.tableWidget.setColumnCount(column_count)
        self.ui.tableWidget.setHorizontalHeaderLabels(column_name)
        for values in data.values():
            row_count = len(values)
            self.ui.tableWidget.setRowCount(row_count)
            column = count
            while column < column_count:
                for rows in range(row_count):
                    item = QtWidgets.QTableWidgetItem(values[rows])
                    self.ui.tableWidget.setItem(rows, column, item)
                column += 1
            count += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = Gui()
    myapp.show()
    sys.exit(app.exec_())
