import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
import mysql.connector
import uuid

# Function to calculate total cost
def calculate_total_cost(price, quantity):
    return price * quantity

class ItemListApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Connect to MySQL database (replace with your credentials)
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="campustock"
            )
            self.cursor = self.connection.cursor()

            # Create itemslist4 table if not exists
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS
                                itemslist4(item_id VARCHAR(36) PRIMARY KEY, item_name TEXT, price REAL, quantity INT, total_cost REAL)""")
            self.connection.commit()

            print("Connected to MySQL database successfully.")
        except mysql.connector.Error as e:
            error_message = "Error connecting to MySQL database: {}".format(e)
            print(error_message)
            QMessageBox.critical(self, "Database Error", error_message)
            sys.exit(1)

        self.items = [
            {"item_id": str(uuid.uuid4()), "item": "Pen", "price": 2},
            {"item_id": str(uuid.uuid4()), "item": "Pencil", "price": 1},
            {"item_id": str(uuid.uuid4()), "item": "Scale", "price": 3},
            {"item_id": str(uuid.uuid4()), "item": "Rounder", "price": 3},
            {"item_id": str(uuid.uuid4()), "item": "Eraser", "price": 1},
            {"item_id": str(uuid.uuid4()), "item": "Single Sided Sheets", "price": 4},
            {"item_id": str(uuid.uuid4()), "item": "Double Sided Sheets", "price": 6},
            {"item_id": str(uuid.uuid4()), "item": "Experiment Headers", "price": 2},
            {"item_id": str(uuid.uuid4()), "item": "Assignment Headers", "price": 2},
            {"item_id": str(uuid.uuid4()), "item": "College Files", "price": 7},
            {"item_id": str(uuid.uuid4()), "item": "Normal Files", "price": 6},
            {"item_id": str(uuid.uuid4()), "item": "Drafter", "price": 8.0},
            {"item_id": str(uuid.uuid4()), "item": "Drawing Books", "price": 10.0},
            {"item_id": str(uuid.uuid4()), "item": "Mechanical Pencils", "price": 2.0},
        ]

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Price", "Quantity", "Total Cost"])

        # Adjust column width
        self.table.setColumnWidth(0, 200)  # Setting the width of the "Item" column

        self.layout = QVBoxLayout()

        for item in self.items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            item_name = QTableWidgetItem(item["item"])
            price = QTableWidgetItem("${:.2f}".format(item["price"]))
            quantity = QLineEdit(self)
            total_cost = QTableWidgetItem("")

            quantity.textChanged.connect(self.calculate_total)  # Connect textChanged signal to calculate_total method

            self.table.setItem(row_position, 0, item_name)
            self.table.setItem(row_position, 1, price)
            self.table.setCellWidget(row_position, 2, quantity)
            self.table.setItem(row_position, 3, total_cost)

        self.proceed_to_order_button = QPushButton("Proceed to Order", self)
        self.proceed_to_order_button.clicked.connect(self.proceed_to_order)

        self.layout.addWidget(self.table)

        # Add a QLabel and QLineEdit for the user's name
        name_label = QLabel("Your Name:", self)
        self.name_input = QLineEdit(self)

        self.layout.addWidget(name_label)
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(self.proceed_to_order_button)

        self.total_cost_label = QLabel("Total Cost: $0.00", self)  # Initialize label with initial total cost
        self.layout.addWidget(self.total_cost_label)

        self.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 400)  # Increased window width
        self.setWindowTitle("Item List")
        self.show()

    def calculate_total(self):
        total_cost = 0
        for row in range(self.table.rowCount()):
            price_text = self.table.item(row, 1).text().replace("$", "")
            quantity_text = self.table.cellWidget(row, 2).text()

            try:
                price = float(price_text)
                quantity = int(quantity_text)  # Convert quantity to an integer
                total = calculate_total_cost(price, quantity)
                total_cost += total
                self.table.item(row, 3).setText("${:.2f}".format(total))
            except ValueError:
                # Handle the case where quantity is not a valid integer
                pass

        self.total_cost_label.setText(f"Total Cost: ${total_cost:.2f}")  # Update the total cost label

    def proceed_to_order(self):
        user_name = self.name_input.text()

        if not user_name:
            QMessageBox.warning(self, "Warning", "Please enter your name.")
            return

        for row in range(self.table.rowCount()):
            item_id = self.items[row]["item_id"]
            item_name = self.table.item(row, 0).text()
            price_text = self.table.item(row, 1).text().replace("$", "")
            quantity_text = self.table.cellWidget(row, 2).text()
            total_cost_text = self.table.item(row, 3).text().replace("$", "")

            try:
                price = float(price_text)
                quantity = int(quantity_text)
                total_cost = float(total_cost_text)

                # Insert the order into the database
                self.cursor.execute("INSERT INTO itemslist4 (item_id, item_name, price, stock, total_cost, user_name) VALUES (%s, %s, %s, %s, %s, %s)",
                                     (item_id, item_name, price, quantity, total_cost, user_name))
                self.connection.commit()
            except ValueError:
                pass

        # Show a message box indicating that the order has been placed
        QMessageBox.information(self, "Order Placed", "Your order has been placed successfully!")

        # Optional: Clear the table, reset total cost label, and clear name input
        self.table.clearContents()
        self.total_cost_label.setText("Total Cost: $0.00")
        self.name_input.clear()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    item_list_app = ItemListApp()
    sys.exit(app.exec_())
