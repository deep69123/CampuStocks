import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.uic import loadUi

from Purchase import PurchaseWindow
from Rentpurchase import RentWindow
from uploade_docs import PrintPage1


class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("admindash.ui", self)

        self.inventory_button.clicked.connect(self.open_inventory)
        self.docs_button.clicked.connect(self.open_docs)
        self.purchases_button.clicked.connect(self.open_purchases)

        self.purchases_window = None  # Initialize PurchaseWindow as None
        self.rent_window = None
        self.print_page = None
    def open_inventory(self):
        if not self.rent_window:  # Check if PurchaseWindow is not already open
            self.rent_window = RentWindow()
        self.rent_window.show()

    def open_docs(self):
        if not self.print_page:  # Check if PurchaseWindow is not already open
            self.print_page = PrintPage1()
        self.print_page.show()
    def open_purchases(self):
        if not self.purchases_window:  # Check if PurchaseWindow is not already open
            self.purchases_window = PurchaseWindow()
        self.purchases_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_dashboard = AdminDashboard()
    admin_dashboard.show()
    sys.exit(app.exec_())
