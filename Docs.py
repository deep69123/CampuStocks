import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout

class DocsWindow(QDialog):
    def __init__(self, documents):
        super().__init__()

        self.documents = documents

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Uploaded Documents")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Display uploaded documents
        for doc in self.documents:
            doc_label = QLabel(doc, self)
            layout.addWidget(doc_label)

        self.setLayout(layout)

if __name__ == '__main__':
    # Sample documents data (replace with actual data from Printout.py)
    documents = ["Document1.pdf", "Document2.docx", "Document3.txt"]

    app = QApplication(sys.argv)
    docs_window = DocsWindow(documents)
    docs_window.show()
    sys.exit(app.exec_())
