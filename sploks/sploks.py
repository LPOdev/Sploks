from PyQt5 import QtWidgets, QtGui, uic
import sys
from controller import menu_controller as menu


# The Ui class is a class that contains all the attributes and methods needed to make the GUI work
class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        """
        This function is used to display the main menu of Sploks
        """
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        menu.displayMenu(self)  # Display the Mainmenu of Sploks
        self.setWindowTitle("Sploks")   # Set the window title to Sploks
        self.setWindowIcon(QtGui.QIcon('views/res/icon.png'))
        self.show()  # Display the app


# This is the main loop of the program. It creates an instance of the Ui class and then runs the app.
app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
window = Ui()  # Create an instance of our class
app.exec_()  # Start the application
