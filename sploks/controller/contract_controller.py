import email
from PyQt5 import QtWidgets, uic
import datetime
import sys

from model.contract import Contract
from model.customer import Customer


def displayContractDetails(contract_id):
    """
    It loads the contract with the given id and displays its details
    
    :param contract_id: The ID of the contract to display
    """
    global w_contract_details
    w_contract_details = uic.loadUi('views/contract_inspector.ui')
    global contract
    contract = Contract()
    contract.load(contract_id)
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

    wContractForm = uic.loadUi('views/contract_form.ui')
    tbl_customers = wContractForm.customers_table
    form_load_customers(Customer.all())

    wContractForm.lbl_name.textChanged.connect(filter_list)
    wContractForm.lbl_firstname.textChanged.connect(filter_list)
    wContractForm.lbl_address.textChanged.connect(filter_list)
    wContractForm.lbl_npa.textChanged.connect(filter_list)
    wContractForm.lbl_town.textChanged.connect(filter_list)
    wContractForm.lbl_phonefix.textChanged.connect(filter_list)
    wContractForm.lbl_phone.textChanged.connect(filter_list)
    wContractForm.lbl_email.textChanged.connect(filter_list)

    tbl_customers.cellClicked.connect(load_customer)

    wContractForm.show()

def form_load_customers(customers):

    tbl_customers.setColumnHidden(0, True)

    for row_number, customer in enumerate(customers): 
        tbl_customers.insertRow(row_number)
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))
            tbl_customers.setItem(row_number, column_number, cell)

def filter_list():
    name = wContractForm.lbl_name.text()
    firstname = wContractForm.lbl_firstname.text()
    address = wContractForm.lbl_address.text()
    npa = wContractForm.lbl_npa.text()
    town = wContractForm.lbl_town.text()
    phonefix = wContractForm.lbl_phonefix.text()
    phone = wContractForm.lbl_phone.text()
    email = wContractForm.lbl_email.text()

    # The above code is a loop that loops through the rows of the table.
    #         It then loops through the columns of the table.
    #         If the text of the cell contains the filter text, then the row is shown.
    #         Otherwise, the row is hidden.
    for x in range(tbl_customers.rowCount()):
        match = False
        
        for y in range(tbl_customers.columnCount()):
            found_name = tbl_customers.item(x,1)
            found_firstname = tbl_customers.item(x,2)
            found_address = tbl_customers.item(x,3)
            found_npa = tbl_customers.item(x,4)
            found_town = tbl_customers.item(x,5)
            found_phonefix = tbl_customers.item(x,6)
            found_phone = tbl_customers.item(x,8)
            found_email = tbl_customers.item(x,7)

            lower_name = (found_name.text()).lower()
            lower_firstname = (found_firstname.text()).lower()
            lower_address = (found_address.text()).lower()
            lower_npa = (found_npa.text()).lower()
            lower_town = (found_town.text()).lower()
            lower_phonefix = (found_phonefix.text()).lower()
            lower_phone = (found_phone.text()).lower()
            lower_email = (found_email.text()).lower()

            if lower_name.find(name.lower()) != -1 and lower_firstname.find(firstname.lower()) != -1 and lower_address.find(address.lower()) != -1 and lower_npa.find(npa.lower()) != -1 and lower_town.find(town.lower()) != -1 and lower_phonefix.find(phonefix.lower()) != -1 and lower_phone.find(phone.lower()) != -1 and lower_email.find(email.lower()) != -1 :
                match = True
                break
                
        tbl_customers.setRowHidden(x, not match)


def load_customer():

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

    tbl_customers.setHidden(True)