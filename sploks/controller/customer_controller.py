from PyQt5 import QtWidgets, uic
from model.customer import Customer

def displayCustomers():
    """
    Loads the .ui file and creates an instance of the object Customer()
    """
    global wCustomers
    global clicked_customer

    wCustomers = uic.loadUi('views/customers_list.ui')  # Load the .ui file
    
    clicked_customer = Customer()  # Creates an instance of the object Customer()
    loadTableCustomers(Customer.all())  # Calls function that displays the data in table
    wCustomers.tableCustomers.horizontalHeader().setSectionResizeMode(1)

    wCustomers.lblSearchBox.textChanged.connect(filter_list)
    
    wCustomers.show()  # Show the window


def displayDetail():
    """
    It displays the details of one customer using its id
    """
    global w_customer_details
    w_customer_details = uic.loadUi('views/customer_inspector.ui')  # Load the .ui file
    global customer_Id
    customer_Id = wCustomers.tableCustomers.item(wCustomers.tableCustomers.currentRow(),
                                                 0).text()  # Get the id of the clicked customer
    clicked_customer.load(customer_Id)  # Calls function that loads data of the customer with his id
    loadCustomerDetails()  # Calls function that displays the data in window with lastname and firstname as customer's identifier

    global contracts_list

    contracts_list = clicked_customer.contracts()
    w_customer_details.lbl_nbContracts.setText(str(len(contracts_list)))

    if len(contracts_list) < 1:
        w_customer_details.btnContracts.setDisabled(True)

    w_customer_details.btnContracts.clicked.connect(customerContracts)

    w_customer_details.show()  # Show the window


def loadTableCustomers(customers):
    """
    It will display the data in the table
    
    :param customers: The list of customers that will be displayed in the table
    """    
    wCustomers.tableCustomers.setColumnHidden(0, True)  # Set the id's column as hidden

    for row_number, customer in enumerate(customers):  # Loop that will display data in the table
        wCustomers.tableCustomers.insertRow(row_number)  # Insert the amount of rows needed
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))  # Initializes the variable as a TableWidget with data
            wCustomers.tableCustomers.setItem(row_number, column_number, cell)  # Add data in the cell of the table
    wCustomers.tableCustomers.cellClicked.connect(
        displayDetail)  # Opens the customer's details' window when clicked in a cell


def loadCustomerDetails():
    """
    It loads the customer details into the customer details window
    """
    w_customer_details.lblNom.setText(str(clicked_customer.lastname))  # Set label's text with the lastname
    w_customer_details.lblPrenom.setText(str(clicked_customer.firstname))  # Set label's text with firstname
    w_customer_details.lblAdresse.setText(str(clicked_customer.address))  # Set label's text with address
    w_customer_details.lblNPA.setText(
        str(clicked_customer.npa) + " " + str(clicked_customer.town))  # Set label's text with NPA and town
    w_customer_details.lblTelephone.setText(str(clicked_customer.phone))  # Set label's text with telephone number
    w_customer_details.lblEmail.setText(str(clicked_customer.email))  # Set label's text with email
    w_customer_details.lblNumero.setText(str(clicked_customer.mobile))  # Set label's text with mobile number


def customerContracts():
    """
    It loads the customer's contracts in the contracts_list table
    """
    global w_customer_contracts
    w_customer_contracts = uic.loadUi('views/contracts_list.ui')
    loadContracts(contracts_list)
    w_customer_contracts.setWindowTitle(f"Contrats de {clicked_customer.firstname} {clicked_customer.lastname}")
    
    w_customer_contracts.tableContracts.horizontalHeader().setSectionResizeMode(1)

    w_customer_contracts.show()


def loadContracts(contracts):
    """
    Load the contracts of the customer in the table
    
    :param contracts: a list of contracts, each one containing the data for a given contract
    """
    w_customer_contracts.tableContracts.setColumnCount(len(contracts[0]))
    w_customer_contracts.tableContracts.setHorizontalHeaderLabels(["Id", "Date de création", "Date de retour", "Notes", "Total", "Assurance", "Service", "Réglage"])

    for row_number, contracts in enumerate(contracts):
        w_customer_contracts.tableContracts.insertRow(row_number)

        for column_number, data in enumerate(contracts):
            cell = QtWidgets.QTableWidgetItem(str(data))
            w_customer_contracts.tableContracts.setItem(row_number, column_number, cell)

def filter_list():
    """
    It loops through each row and column of the table and checks if the text in the search box is found
    in the table. If it is, it shows the row. If not, it hides the row
    """
    filter_txt = wCustomers.lblSearchBox.text()

    for x in range(wCustomers.tableCustomers.rowCount()):
        match = False
        for y in range(wCustomers.tableCustomers.columnCount()):
            found_item = wCustomers.tableCustomers.item(x,y)
            txt = (found_item.text()).lower()
            if txt.find(filter_txt.lower()) != -1:
                match = True
                break
                
        wCustomers.tableCustomers.setRowHidden(x, not match)