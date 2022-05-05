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

    wContractForm = uic.loadUi('views/contract_form.ui')
    form_load_customers(Customer.all())

    wContractForm.lbl_name.textChanged.connect(filter_list)
    wContractForm.lbl_firstname.textChanged.connect(filter_list)
    wContractForm.lbl_address.textChanged.connect(filter_list)
    wContractForm.lbl_npa.textChanged.connect(filter_list)
    wContractForm.lbl_town.textChanged.connect(filter_list)
    wContractForm.lbl_phonefix.textChanged.connect(filter_list)
    wContractForm.lbl_phone.textChanged.connect(filter_list)
    wContractForm.lbl_email.textChanged.connect(filter_list)

    wContractForm.show()

def form_load_customers(customers):

    wContractForm.customers_table.setColumnHidden(0, True)

    for row_number, customer in enumerate(customers): 
        wContractForm.customers_table.insertRow(row_number)
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))
            wContractForm.customers_table.setItem(row_number, column_number, cell)

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
    for x in range(wContractForm.customers_table.rowCount()):
        match = False
        
        for y in range(wContractForm.customers_table.columnCount()):
            found_name = wContractForm.customers_table.item(x,1)
            found_firstname = wContractForm.customers_table.item(x,2)
            found_address = wContractForm.customers_table.item(x,3)
            found_npa = wContractForm.customers_table.item(x,4)
            found_town = wContractForm.customers_table.item(x,5)
            found_phonefix = wContractForm.customers_table.item(x,6)
            found_phone = wContractForm.customers_table.item(x,7)
            found_email = wContractForm.customers_table.item(x,8)

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
                
        wContractForm.customers_table.setRowHidden(x, not match)
