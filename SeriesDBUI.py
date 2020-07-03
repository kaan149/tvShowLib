import os
import sys
from PyQt5 import QtWidgets
import Library
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QHBoxLayout, \
    QWidget, qApp, QTableWidget, QTableWidgetItem, QMessageBox, QMenu, QDesktopWidget


class Series(QWidget):

    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        self.refresh = QPushButton("Load/Refresh")
        self.order_bn = QPushButton("Order (by name)")
        self.order_bt = QPushButton("Order (by type)")
        self.order_bs = QPushButton("Order (by season)")
        self.transfer = QPushButton("Transfer to txt")
        self.add = QPushButton("Add")
        self.delete = QPushButton("Delete")
        self.init_ui()
        self.lib = Library.Library()

    def init_ui(self):
        h_box = QHBoxLayout()

        h_box.addWidget(self.add)
        h_box.addWidget(self.delete)
        h_box.addWidget(self.order_bn)
        h_box.addWidget(self.order_bt)
        h_box.addWidget(self.order_bs)
        h_box.addWidget(self.refresh)
        h_box.addWidget(self.transfer)

        v_box = QVBoxLayout()

        v_box.addWidget(self.table)

        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.setWindowTitle("TV Show Library")
        self.add.clicked.connect(self.add_series)
        self.delete.clicked.connect(self.remove_series)
        self.order_bn.clicked.connect(self.order_data_bn)
        self.order_bt.clicked.connect(self.order_data_bt)
        self.order_bs.clicked.connect(self.order_data_bs)
        self.refresh.clicked.connect(self.load_data)
        self.transfer.clicked.connect(self.copy_data)

    def data_connection(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels(("Name of series", "Type of series", "Number of seasons"))

        header = self.table.horizontalHeader()

        size_row = len(data)
        size_col = len(data[0])

        for i in range(size_col):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        for row in range(size_row):
            for column in range(size_col):
                self.table.setItem(row, column, QTableWidgetItem(str(data[row][column])))
                self.table.setItem(row, column + 1, QTableWidgetItem(str(data[row][column])))
                self.table.setItem(row, column + 2, QTableWidgetItem(str(data[row][column])))

    def copy_data(self):
        file_name = QFileDialog.getSaveFileName(self, "Save File", os.getenv("HOME"))

        with open(file_name[0], "w") as file:
            data = self.lib.show_the_series()
            for i in data:
                line = ' '.join(str(x) for x in i)
                file.write(line + '\n')

    def load_data(self):
        data = self.lib.show_the_series()
        self.data_connection(data)

    def order_data_bn(self):
        data = self.lib.order_by_alphabetic()
        self.data_connection(data)

    def order_data_bt(self):
        data = self.lib.order_by_type()
        self.data_connection(data)

    def order_data_bs(self):
        data = self.lib.order_by_seasons()
        self.data_connection(data)

    def add_series(self):
        self.aw = AdditionWindow()

    def remove_series(self):
        self.rw = RemovingWindow()


class Menu(QMainWindow):

    def __init__(self):

        super().__init__()

        self.window = Series()

        self.setCentralWidget(self.window)

        self.top = 400
        self.left = 400
        self.width = 1200
        self.height = 800

        self.create_menu()

    def create_menu(self):

        self.setGeometry(self.top, self.left, self.width, self.height)
        self.center()
        menubar = self.menuBar()

        options = menubar.addMenu("Options")

        add_series = QAction("Add Series", self)
        add_series.setShortcut("Ctrl+I")

        remove_series = QAction("Remove Series", self)
        remove_series.setShortcut("Ctrl+R")

        sort = QMenu("Sort", self)

        exit0 = QAction("Exit", self)
        exit0.setShortcut("Ctrl+Q")

        options.addAction(add_series)
        options.addAction(remove_series)
        options.addMenu(sort)
        options.addAction(exit0)

        sort_n = QAction("By name", self)
        sort_t = QAction("By type", self)
        sort_s = QAction("By number of seasons", self)

        sort.addAction(sort_n)
        sort.addAction(sort_t)
        sort.addAction(sort_s)
        options.triggered.connect(self.response)

        self.setWindowTitle("TV Show Library")

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def response(self, action):

        if action.text() == "Add Series":
            self.aw = AdditionWindow()

        elif action.text() == "Remove Series":
            self.rw = RemovingWindow()

        elif action.text() == "By name":
            self.pencere.order_data_bn()

        elif action.text() == "By type":
            self.pencere.order_data_bt()

        elif action.text() == "By number of seasons":
            self.pencere.order_data_bs()

        elif action.text() == "Exit":
            qApp.quit()


class AdditionWindow(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.button = QPushButton("Insert Data", self)
        self.season = QtWidgets.QLineEdit()
        self.type = QtWidgets.QLineEdit()
        self.name = QtWidgets.QLineEdit()
        self.lib = Library.Library()
        self.top = 200
        self.left = 200
        self.width = 600
        self.height = 200

        self.adding_part()

    def adding_part(self):

        self.setGeometry(self.top, self.left, self.width, self.height)

        self.name.setPlaceholderText("Name of the series")

        self.type.setPlaceholderText("Type of the series")

        self.season.setPlaceholderText("Number of seasons")

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.name)
        v_box.addWidget(self.type)
        v_box.addWidget(self.season)
        v_box.addWidget(self.button)
        self.button.clicked.connect(self.insert_data)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()

        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.setWindowTitle("Add Series")
        self.show()

    def insert_data(self):

        series = Library.Series(self.name.text().lower(), self.type.text().lower(), self.season.text())
        data = self.lib.show_the_series()
        x = list()
        for i in data:
            x.append(i[0])

        if x.__contains__(self.name.text().lower()):
            QMessageBox.about(self, "Error", "This tv show already in your library")
        else:
            self.lib.add_series0(series)
            QMessageBox.about(self, "Successfully", 'Data inserted successfully')


class RemovingWindow(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.button = QPushButton("Remove Data", self)
        self.name = QtWidgets.QLineEdit()
        self.lib = Library.Library()
        self.top = 200
        self.left = 200
        self.width = 600
        self.height = 200

        self.removing_part()

    def removing_part(self):

        self.setGeometry(self.top, self.left, self.width, self.height)

        self.name.setPlaceholderText("Name of the series")

        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(self.name)
        v_box.addWidget(self.button)
        self.button.clicked.connect(self.remove_data)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()

        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.setWindowTitle("Remove Series")
        self.show()

    def remove_data(self):
        data = self.lib.show_the_series()
        x = list()
        for i in data:
            x.append(i[0])

        if x.__contains__(self.name.text().lower()):
            self.lib.remove_series0(self.name.text())
            QMessageBox.about(self, "Successfully", 'Data removed successfully')
        else:
            QMessageBox.about(self, "Error", 'This tv show is not in your library')


app = QApplication(sys.argv)
menu = Menu()
sys.exit(app.exec_())


