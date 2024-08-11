import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import mysql.connector as mycon
from DashBoard import Dashboard
from AdminDashboard import AdminDashboard  # Import AdminDashboard class

class Login(QDialog):
    loginSuccessful = QtCore.pyqtSignal()  # Define a signal for successful login
    designationSelected = QtCore.pyqtSignal(str)  # Signal to send the selected designation

    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.verify.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.open_registration)

        # Populate the designation dropdown
        self.designation.addItems(["Admin", "Student"])

    def loginfunction(self):
        try:
            username = self.username.text()
            password = self.password.text()
            designation = self.designation.currentText()  # Get the selected designation from the dropdown

            if not all([username, password]):  # Check if any of the fields are empty
                print("Fill the empty spaces")
                return

            mydb = mycon.connect(host="localhost", user="root", password="", database="pyqt5_login")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM log_db WHERE PID=%s AND password1=%s AND designation=%s ", (username, password, designation))
            result = mycursor.fetchone()

            if result:
                print("Login successful")
                self.loginSuccessful.emit()
                self.designationSelected.emit(designation)  # Emit the selected designation

            else:
                print("Invalid information")
        except mycon.Error as e:
            print("local host not connected")

    def open_registration(self):
        createacc = CreateAcc()
        createacc.signupClicked.connect(self.back_to_login)  # Connect the signal to a slot
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_to_login(self):
        widget.setCurrentIndex(0)  # Set current index to login page

class CreateAcc(QDialog):
    signupClicked = QtCore.pyqtSignal()  # Define a signal

    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("register.ui", self)
        self.signup.clicked.connect(self.createaccfunction)
        self.password1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.designation.addItems(["Admin", "Student"])

    def createaccfunction(self):
        try:
            username = self.username.text()
            email = self.email.text()
            phone = self.phone.text()
            branch = self.branch.text()
            designation = self.designation.currentText()  # Get the selected designation from the dropdown

            if not all([username, email, phone, branch, self.password1.text(), self.password2.text()]):  # Check if any of the fields are empty
                print("Fill all the required fields")
                return

            # Email validation
            if "@" not in email:
                print("The email is invalid")
                return

            # Password validation
            if len(self.password1.text()) < 8:
                print("The password is too short. The password should have at least 8 characters")
                return

            # Username (PID) validation
            if len(username) != 6:
                print("Invalid PID")
                return

            if self.password1.text() == self.password2.text():
                password = self.password1.text()
                designation = self.designation.currentText()
                print("Successfully created account with role:", designation)
                self.signupClicked.emit()
            else:
                print("Passwords don't match")

            mydb = mycon.connect(host="localhost", user="root", password="", database="pyqt5_login")
            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT * FROM log_db WHERE phone= %s AND email= %s AND branch= %s AND PID= %s AND password1 = %s AND designation = %s",
                (phone, email, branch, username, password, designation))
            result = mycursor.fetchone()

            if result:
                print("Already exists")
            else:
                mycursor.execute(
                    "INSERT INTO log_db (PID, email, phone, branch, password1, designation) VALUES (%s, %s, %s, %s, %s, %s)",
                    (username, email, phone, branch, password, designation))
                mydb.commit()
                print("Completed")

        except mycon.Error as e:
            print("Local host not connected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainwindow = Login()
    mainwindow.setWindowTitle("Login")
    mainwindow.setFixedSize(1100,800)
    widget.addWidget(mainwindow)
    widget.show()

    # Create instances of Dashboard and AdminDashboard
    dashboard = Dashboard()
    admin_dashboard = AdminDashboard()

    # Connect the signals from Login to switch between the appropriate dashboards
    mainwindow.loginSuccessful.connect(dashboard.show)
    mainwindow.designationSelected.connect(lambda designation: admin_dashboard.show() if designation == "Admin" else dashboard.show())

    sys.exit(app.exec_())
