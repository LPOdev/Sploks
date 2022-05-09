import email
from PyQt5 import QtWidgets, uic, QtGui

from model.contract import Contract
from model.customer import Customer


def displayContractDetails(contract_id):
    """
    It loads the contract with the given id and displays its details
    
    :param contract_id: The ID of the contract to display
    """
    global w_contract_details
    global contract
    
    contract = Contract()
    contract.load(contract_id)

    w_contract_details = uic.loadUi('views/contract_inspector.ui')
    
    insertDetails()
    w_contract_details.setWindowTitle(f"Contrat {contract.id} du {contract.creation_date} avec {contract.firstname} {contract.lastname}")
    w_contract_details.show()    

def insertDetails():
    """
    It takes the contract object and displays its details in the contract details window
    """
    w_contract_details.lbl_id.setText(str(contract.id))
    w_contract_details.lbl_creationDate.setText(contract.creation_date)
    w_contract_details.lbl_returnDate.setText(contract.effective_return)
    w_contract_details.lst_lastname.addItem(contract.lastname)
    w_contract_details.lst_firstname.addItem(contract.firstname)
    w_contract_details.lst_phone.addItem(contract.phone)
    w_contract_details.lst_address.addItem(contract.address)
    w_contract_details.lst_town.addItem(contract.town)
    w_contract_details.lst_mobile.addItem(contract.mobile)
    w_contract_details.lst_email.addItem(contract.email)

########## - Contract Form - ##########

def displayForm():
    global wContractForm
    global tbl_customers
    global tbl_items

    wContractForm = uic.loadUi('views/contract_form.ui')

    tbl_customers = wContractForm.customers_table
    tbl_items = wContractForm.equipement_table
    form_load_customers(Customer.all())

    # Hide Item Form
    tbl_items.setHidden(True)
    wContractForm.label_21.setHidden(True)

    wContractForm.lbl_name.textChanged.connect(filter_list)
    wContractForm.lbl_firstname.textChanged.connect(filter_list)
    wContractForm.lbl_address.textChanged.connect(filter_list)
    wContractForm.lbl_npa.textChanged.connect(filter_list)
    wContractForm.lbl_town.textChanged.connect(filter_list)
    wContractForm.lbl_phonefix.textChanged.connect(filter_list)
    wContractForm.lbl_phone.textChanged.connect(filter_list)
    wContractForm.lbl_email.textChanged.connect(filter_list)

    tbl_customers.cellClicked.connect(load_customer)

    ### Shortcuts ###
    shrtClients = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+d'), wContractForm)    # Create the shortcut
    shrtClients.activated.connect(shortcut_used)   # Connect the shortcut
    ### Shortcuts ###

    wContractForm.show()

def form_load_customers(customers):

    tbl_customers.setColumnHidden(0, True)

    for row_number, customer in enumerate(customers): 
        tbl_customers.insertRow(row_number)
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))
            tbl_customers.setItem(row_number, column_number, cell)

def filter_list():
    search_client = {
        "name": (wContractForm.lbl_name.text()).lower(),
        "firstname": (wContractForm.lbl_firstname.text()).lower(),
        "address": (wContractForm.lbl_address.text()).lower(),
        "npa": (wContractForm.lbl_npa.text()).lower(),
        "town": (wContractForm.lbl_town.text()).lower(),
        "phonefix": (wContractForm.lbl_phonefix.text()).lower(),
        "email": (wContractForm.lbl_email.text()).lower(),
        "phone": (wContractForm.lbl_phone.text()).lower()
        
    }
    match = False

    found_client = {}

    for x in range(tbl_customers.rowCount()):
        
        for y in range(tbl_customers.columnCount()):
            match y:
                case 1:
                    found_client['name'] = (tbl_customers.item(x, y).text()).lower()
                case 2:
                    found_client['firstname'] = (tbl_customers.item(x, y).text()).lower()
                case 3:
                    found_client['address'] = (tbl_customers.item(x, y).text()).lower()
                case 4:
                    found_client['npa'] = (tbl_customers.item(x, y).text()).lower()
                case 5:
                    found_client['town'] = (tbl_customers.item(x, y).text()).lower()
                case 6:
                    found_client['phonefix'] = (tbl_customers.item(x, y).text()).lower()
                case 7:
                    found_client['email'] = (tbl_customers.item(x, y).text()).lower()
                case 8:
                    found_client['phone'] = (tbl_customers.item(x, y).text()).lower()

        for f, s in zip(found_client, search_client):
            if found_client[f].find(search_client[s]) != -1:
                match = True
            else:
                match = False
                break
        
        tbl_customers.setRowHidden(x, not match)

def shortcut_used():
    if(tbl_customers.item(tbl_customers.currentRow(), 0) != None):
        load_customer()

def load_customer():
    openItemslist()
    clicked_id = tbl_customers.item(tbl_customers.currentRow(), 0).text()

    customer = Customer()
    customer.load(clicked_id)

    name = wContractForm.lbl_name.setText(str(customer.lastname))
    firstname = wContractForm.lbl_firstname.setText(str(customer.firstname))
    address = wContractForm.lbl_address.setText(str(customer.address))
    npa = wContractForm.lbl_npa.setText(str(customer.npa))
    town = wContractForm.lbl_town.setText(str(customer.town))
    phonefix = wContractForm.lbl_phonefix.setText(str(customer.phone))
    phone = wContractForm.lbl_phone.setText(str(customer.mobile))
    email = wContractForm.lbl_email.setText(str(customer.email))

    """tbl_customers.setHidden(True)
    tbl_items.setHidden(False)
    wContractForm.label_21.setHidden(False)
    """
    openItemslist()


def openItemslist():
    wlisttesting = uic.loadUi('views/contract_items.ui')

    wlisttesting.show()