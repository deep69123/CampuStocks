import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout

class InventoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Items from ItemsList.py and RentList.py
        self.items = [
            {"item": "Pen", "price": 1.5, "stock_available": 100},
            {"item": "Pencil", "price": 0.8, "stock_available": 150},
            {"item": "Scale", "price": 2.5, "stock_available": 80},
            {"item": "Rounder", "price": 3.0, "stock_available": 50},
            {"item": "Eraser", "price": 0.5, "stock_available": 200},
            {"item": "Single Sided Sheets", "price": 4.0, "stock_available": 120},
            {"item": "Double Sided Sheets", "price": 6.0, "stock_available": 100},
            {"item": "Experiment Headers", "price": 2.0, "stock_available": 70},
            {"item": "Assignment Headers", "price": 1.5, "stock_available": 90},
            {"item": "College Files", "price": 7.0, "stock_available": 60},
            {"item": "Normal Files", "price": 5.5, "stock_available": 80},
            {"item": "Drafter", "price": 8.0, "stock_available": 40},
            {"item": "Drawing Books", "price": 10.0, "stock_available": 50},
            {"item": "Mechanical Pencils", "price": 2.0, "stock_available": 100},
        ]

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Price", "Stock", "Stock Available"])

        self.layout = QVBoxLayout()

        for item in self.items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            item_name = QTableWidgetItem(item["item"])
            price = QLineEdit("${:.2f}".format(item["price"]))
            stock = QLineEdit("0")  # Initial stock value
            stock_available = QLineEdit(str(item["stock_available"]))

            # Set the price field as editable
            price.setReadOnly(False)

            # Buttons to increase and decrease stock
            plus_button = QPushButton("+")
            plus_button.clicked.connect(lambda _, row=row_position: self.modify_stock(row, 1))
            minus_button = QPushButton("-")
            minus_button.clicked.connect(lambda _, row=row_position: self.modify_stock(row, -1))

            self.table.setItem(row_position, 0, item_name)
            self.table.setCellWidget(row_position, 1, price)
            self.table.setCellWidget(row_position, 2, stock)
            self.table.setCellWidget(row_position, 3, stock_available)
            self.table.setCellWidget(row_position, 4, plus_button)
            self.table.setCellWidget(row_position, 5, minus_button)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Inventory")
        self.show()

    def modify_stock(self, row, change):
        # Get the current stock value from the table
        current_stock = int(self.table.cellWidget(row, 2).text())
        new_stock = current_stock + change
        if new_stock >= 0:
            self.table.cellWidget(row, 2).setText(str(new_stock))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    inventory = InventoryWindow()
    sys.exit(app.exec_())
