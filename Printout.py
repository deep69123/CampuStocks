import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QFileDialog, QVBoxLayout
import os
import shutil

class PrintPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.pages_label = QLabel("Select Pages:")
        self.pages_edit = QComboBox(self)
        self.pages_edit.addItems(["All", "Current Page", "Page Range"])

        self.copies_label = QLabel("Number of Copies:")
        self.copies_edit = QComboBox(self)
        self.copies_edit.addItems([str(i) for i in range(1, 11)])  # Options from 1 to 10

        self.color_label = QLabel("Color Mode:")
        self.color_edit = QComboBox(self)
        self.color_edit.addItems(["Black/White", "Color"])

        self.layout_label = QLabel("Layout:")
        self.layout_edit = QComboBox(self)
        self.layout_edit.addItems(["Portrait", "Landscape"])

        self.upload_button = QPushButton("Upload Document", self)
        self.upload_button.clicked.connect(self.upload_document)

        self.print_button = QPushButton("Print", self)
        self.print_button.clicked.connect(self.print_document)

        layout = QVBoxLayout()
        layout.addWidget(self.pages_label)
        layout.addWidget(self.pages_edit)
        layout.addWidget(self.copies_label)
        layout.addWidget(self.copies_edit)
        layout.addWidget(self.color_label)
        layout.addWidget(self.color_edit)
        layout.addWidget(self.layout_label)
        layout.addWidget(self.layout_edit)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Print Page")

    def upload_document(self):
        options = "PDF (*.pdf);;PowerPoint (*.ppt *.pptx);;Word (*.doc *.docx);;Excel (*.xls *.xlsx);;JPEG (*.jpeg *.jpg);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Document", "", options)
        if file_path:
            print("File uploaded:", file_path)
            # Specify the directory where you want to store the uploaded documents
            upload_dir = "uploaded_documents"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            # Get the filename from the file path
            filename = os.path.basename(file_path)
            # Construct the destination path
            destination_path = os.path.join(upload_dir, filename)
            # Copy the file to the destination path
            try:
                shutil.copy(file_path, destination_path)
                print("File saved to:", destination_path)
            except Exception as e:
                print("Error:", e)

    def print_document(self):
        # Implement printing logic here
        print("Printing...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print_page = PrintPage()
    print_page.show()
    sys.exit(app.exec_())
