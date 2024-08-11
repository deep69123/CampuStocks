import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import os

class PrintPage1(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.view_button = QPushButton("View Uploaded Documents", self)
        self.view_button.clicked.connect(self.view_uploaded_documents)

        layout = QVBoxLayout()
        layout.addWidget(self.view_button)

        self.setLayout(layout)

        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle("Print Page")

    def view_uploaded_documents(self):
        upload_dir = "uploaded_documents"
        if os.path.exists(upload_dir):
            os.startfile(upload_dir)  # Opens the directory using the default file explorer
        else:
            print("No documents uploaded yet.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print_page = PrintPage1()
    print_page.show()
    sys.exit(app.exec_())
