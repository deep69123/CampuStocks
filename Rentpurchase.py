import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
import mysql.connector

class RentWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Rent Transaction")
        self.setGeometry(1000, 100, 700, 800)

        # Connect to MySQL database (replace with your credentials)
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="campustock"
            )
            self.cursor = self.connection.cursor()

            print("Connected to MySQL database successfully.")
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)
            sys.exit(1)

        self.table = QTableWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.populate_table()

    def populate_table(self):
        # Fetch data from the database
        try:
            self.cursor.execute("SELECT * FROM rent")
            data = self.cursor.fetchall()

            # Set table dimensions based on the number of rows and columns in the fetched data
            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data[0]))

            # Populate table with fetched data
            for row_num, row_data in enumerate(data):
                for col_num, cell_data in enumerate(row_data):
                    self.table.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

            # Set table headers
            self.table.setHorizontalHeaderLabels(["Name","Rent ID", "Item Name", "Price Per Week", "Number of Weeks", "Total Cost"])

        except mysql.connector.Error as e:
            print("Error fetching data from MySQL database:", e)

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rent_window = RentWindow()
    rent_window.show()
    sys.exit(app.exec_())
