import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt5.uic import loadUi

from ItemsList import ItemListApp
from Printout import PrintPage
from RentList import RentList

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.item_list_app = None
        self.rent_list_app = None
        self.print_page = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")

        # Load the UI from dashboard.ui
        loadUi("dashboard.ui", self)

        # Connect button clicks to respective functions
        self.rent_button.clicked.connect(self.open_rent_list)
        self.buy_button.clicked.connect(self.open_item_list)
        self.printout_button.clicked.connect(self.open_print_page)

    def open_rent_list(self):
        if not self.rent_list_app:  # Check if ItemListApp is not already open
            self.rent_list_app = RentList()
        self.rent_list_app.show()

    def open_item_list(self):
        if not self.item_list_app:  # Check if ItemListApp is not already open
            self.item_list_app = ItemListApp()
        self.item_list_app.show()

    def open_print_page(self):
        if not self.print_page:  # Check if ItemListApp is not already open
            self.print_page = PrintPage()
        self.print_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    dashboard.setWindowTitle("Dashboard")
    dashboard.setFixedSize(1200, 800)
    sys.exit(app.exec_())