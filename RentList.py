import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import uuid

# Function to calculate total cost
def calculate_total_cost(price_per_week, num_weeks):
    return price_per_week * num_weeks

class RentList(QWidget):
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

            # Create rent table if not exists
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS
                                rent(rent_id VARCHAR(36) PRIMARY KEY, item_name TEXT, price_per_week REAL, num_weeks INT, total_cost REAL, user_name TEXT)""")
            self.connection.commit()

            print("Connected to MySQL database successfully.")
        except mysql.connector.Error as e:
            error_message = "Error connecting to MySQL database: {}".format(e)
            print(error_message)
            QMessageBox.critical(self, "Database Error", error_message)
            sys.exit(1)

        self.items = [
            {"item": "Drafter", "price_per_week": 5.0},
            {"item": "Apron", "price_per_week": 8.0},
            {"item": "Containers", "price_per_week": 8.0},
            {"item": "Lab coats", "price_per_week": 8.0},
            {"item": "GPS equipment", "price_per_week": 8.0},
            {"item": "Multimeter", "price_per_week": 6.0},
            {"item": "Oscilloscpoes", "price_per_week": 10.0},
            {"item": "Forklifts", "price_per_week": 9.0},
        ]

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Price Per Week", "No. of Weeks", "Total Cost"])

        # Adjust column width
        self.table.setColumnWidth(0, 150)  # Setting the width of the "Item" column

        self.layout = QVBoxLayout()

        for item in self.items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            item_name = QTableWidgetItem(item["item"])
            price_per_week = QTableWidgetItem("${:.2f}".format(item["price_per_week"]))
            num_weeks = QLineEdit(self)
            total_cost = QTableWidgetItem("")

            self.table.setItem(row_position, 0, item_name)
            self.table.setItem(row_position, 1, price_per_week)
            self.table.setCellWidget(row_position, 2, num_weeks)
            self.table.setItem(row_position, 3, total_cost)

            num_weeks.textChanged.connect(self.calculate_total)  # Connect textChanged signal to calculate_total method

        self.proceed_to_rent_button = QPushButton("Proceed to Rent", self)
        self.proceed_to_rent_button.clicked.connect(self.proceed_to_rent)
        self.proceed_to_rent_button.setFixedSize(100, 100)  # Set fixed size for the button

        self.layout.addWidget(self.table)

        # Add a QLabel and QLineEdit for the user's name
        name_label = QLabel("Your Name:", self)
        self.name_input = QLineEdit(self)

        self.layout.addWidget(name_label)
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(self.proceed_to_rent_button)

        self.total_sum_label = QLabel("", self)
        self.layout.addWidget(self.total_sum_label)

        self.setLayout(self.layout)

        self.setWindowTitle("Rent List")

        # Calculate screen center
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        # Convert x and y to integers
        x = int(x)
        y = int(y)

        self.move(x, y)  # Move the widget to the center of the screen

        # Set window size
        self.setGeometry(1000, 100, 700, 800)

    def calculate_total(self):
        total_cost = 0
        for row in range(self.table.rowCount()):
            price_per_week = float(self.table.item(row, 1).text().replace("$", ""))
            num_weeks_text = self.table.cellWidget(row, 2).text()
            if not num_weeks_text:
                self.table.item(row, 3).setText("")  # Clear the total cost field
                continue
            try:
                num_weeks = float(num_weeks_text)
                if num_weeks < 0:
                    raise ValueError("Number of weeks cannot be negative")
                total = calculate_total_cost(price_per_week, num_weeks)
                total_cost += total
                self.table.item(row, 3).setText("${:.2f}".format(total))
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
                return

        total_sum = sum(float(self.table.item(row, 3).text().replace("$", ""))
                        for row in range(self.table.rowCount())
                        if self.table.item(row, 3).text())

        self.total_sum_label.setText(f"Total Sum: ${total_sum:.2f}")

    def proceed_to_rent(self):
        user_name = self.name_input.text()  # Get the user's name
        if not user_name:
            QMessageBox.warning(self, "Warning", "Please enter your name.")
            return

        for row in range(self.table.rowCount()):
            rent_id = str(uuid.uuid4())
            item_name = self.items[row]["item"]
            price_per_week_text = self.table.item(row, 1).text().replace("$", "")
            num_weeks_text = self.table.cellWidget(row, 2).text()
            total_cost_text = self.table.item(row, 3).text().replace("$", "")

            try:
                price_per_week = float(price_per_week_text)
                num_weeks = int(num_weeks_text)
                total_cost = float(total_cost_text)

                self.cursor.execute("INSERT INTO rent (rent_id, item_name, price_per_week, num_weeks, total_cost, user_name) VALUES (%s, %s, %s, %s, %s, %s)",
                                     (rent_id, item_name, price_per_week, num_weeks, total_cost, user_name))
                self.connection.commit()
            except ValueError:
                pass

        QMessageBox.information(self, "Rent Placed", "Your rent has been placed successfully!")

        self.table.clearContents()
        self.total_sum_label.setText("Total Sum: $0.00")
        self.name_input.clear()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rent_list_app = RentList()
    rent_list_app.show()
    sys.exit(app.exec_())
