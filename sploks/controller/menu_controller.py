from PyQt5 import QtWidgets, QtGui, uic
import sys
from controller import customer_controller as clients
from controller import staff_controller as staffs
from controller import stock_controller as stocks
from controller import contract_controller as contracts

sploks_version = "0.8.0"

def displayMenu(self):
    """
    Display the menu.
    """
    global wMenu
    wMenu = uic.loadUi('views/menu.ui', self)  # Load the .ui file
    wMenu.btnClients.clicked.connect(getClients)  # Open the list of clients
    wMenu.btnStaff.clicked.connect(getStaffs)  # Open the list of staffs
    wMenu.btnStock.clicked.connect(getStock)  # Open the list of item
    wMenu.btnNewContract.clicked.connect(getContractForm)
    wMenu.btnContracts.clicked.connect(getContracts)

    ### Shortcuts ###
    # It creates a shortcut to open the list of clients.
    shrtClients = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+C'), self)    # Create the shortcut
    shrtClients.activated.connect(getClients)   # Connect the shortcut

    # It creates a shortcut to open the list of staffs.
    shrtStaff = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+P'), self)  # Create the shortcut
    shrtStaff.activated.connect(getStaffs)  # Connect the shortcut

    # It creates a shortcut to open the list of item.
    shrtStock = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+I'), self) # Create the shortcut
    shrtStock.activated.connect(getStock)   # Connect the shortcut
    ### Shortcuts ###

    # Insert sploks version into label
    wMenu.lblVersion.setText(sploks_version)

    wMenu.show()  # Show the menu


def getClients():
    """
    This function displays all the customers in the database
    """
    clients.displayCustomers()


def getStaffs():
    """
    This function displays all the staffs in the staffs list
    """
    staffs.displayStaffs()


def getStock():
    """
    This function displays the stock
    """
    stocks.displayStock()

def getContracts():
    contracts.displayContracts()

def getContractForm():
    contracts.displayForm()
