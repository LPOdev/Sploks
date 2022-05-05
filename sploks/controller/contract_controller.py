from PyQt5 import QtWidgets, uic
import datetime
import sys

from model.contract import Contract


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

def displayForm():
    global wContractForm
    wContractForm = uic.loadUi('views/contract_form.ui')
    wContractForm.show()

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


