from datetime import datetime
from PyQt5 import QtWidgets, QtGui,uic

from model.contract import Contract
from model.customer import Customer
from model.helpers import Helpers
from model.item import Item
from model.state import State
from model.duration import Duration

def displayContracts():
    """
    This function displays the contracts of one item
    """
    global wContracts

    wContracts = uic.loadUi('views/contracts_list.ui')    
    wContracts.tableContracts.horizontalHeader().setSectionResizeMode(1)
    
    ls_contracts = Contract.allWithParams()
    loadContracts(ls_contracts)

    wContracts.lblSearchBox.textChanged.connect(filter_list)

    wContracts.chk_late.stateChanged.connect(lambda: show_late(ls_contracts))

    wContracts.show()


def loadContracts(contracts_list):
    
    wContracts.tableContracts.setColumnCount(len(contracts_list[0])-1)
    wContracts.tableContracts.setHorizontalHeaderLabels(["Id", "Client", "Date", "Retour"])
    wContracts.chk_late.setDisabled(False)

    for row_number, contracts in enumerate(contracts_list):
        wContracts.tableContracts.insertRow(row_number)

        for column_number, data in enumerate(contracts[:-1]):
            cell = QtWidgets.QTableWidgetItem(str(data))
            wContracts.tableContracts.setItem(row_number, column_number, cell)
        
        if contracts[4] is None:
            if datetime.strptime(contracts[3], '%d.%m.%Y') < datetime.now():
                wContracts.tableContracts.item(row_number, 3).setForeground(QtGui.QColor(255, 0, 0))          

        else:
            if datetime.strptime(contracts[3], '%d.%m.%Y') > datetime.strptime(contracts[4], '%d.%m.%Y'):
                wContracts.tableContracts.item(row_number, 3).setForeground(QtGui.QColor(0, 128, 0))
            
            elif datetime.strptime(contracts[3], '%d.%m.%Y') < datetime.strptime(contracts[4], '%d.%m.%Y'):
                wContracts.tableContracts.item(row_number, 3).setForeground(QtGui.QColor(255, 0, 255))

    wContracts.tableContracts.setColumnHidden(0, True)

def show_late(contracts_list):

    if wContracts.chk_late.checkState():
        for row_number, contracts in enumerate(contracts_list):
            match = False

            if contracts[4] is None and datetime.strptime(contracts[3], '%d.%m.%Y') < datetime.now():
                match = True

            wContracts.tableContracts.setRowHidden(row_number, not match)
    else:
        for row_number, contracts in enumerate(contracts_list):
            wContracts.tableContracts.setRowHidden(row_number, False)
    
def filter_list():
    wContracts.chk_late.setDisabled(True)
    wContracts.chk_late.setCheckState(False)

    filter_txt = wContracts.lblSearchBox.text()

    if filter_txt == "":
        wContracts.chk_late.setDisabled(False)

    for x in range(wContracts.tableContracts.rowCount()):
        match = False
        for y in range(wContracts.tableContracts.columnCount()):
            found_item = wContracts.tableContracts.item(x,y)
            txt = (found_item.text()).lower()
            if txt.find(filter_txt.lower()) != -1:
                match = True
                break
                
        wContracts.tableContracts.setRowHidden(x, not match)

########## - Contract Details - ##########

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
    w_contract_details.setWindowTitle(
        f"Contrat {contract.id} du {contract.creation_date} avec {contract.firstname} {contract.lastname}")
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
    wContractForm.btn_openList.setHidden(True)
    wContractForm.btn_delete.setHidden(True)


    wContractForm.lbl_name.textChanged.connect(filter_list_clients)
    wContractForm.lbl_firstname.textChanged.connect(filter_list_clients)
    wContractForm.lbl_address.textChanged.connect(filter_list_clients)
    wContractForm.lbl_npa.textChanged.connect(filter_list_clients)
    wContractForm.lbl_town.textChanged.connect(filter_list_clients)
    wContractForm.lbl_phonefix.textChanged.connect(filter_list_clients)
    wContractForm.lbl_phone.textChanged.connect(filter_list_clients)
    wContractForm.lbl_email.textChanged.connect(filter_list_clients)

    tbl_customers.cellClicked.connect(load_customer)

    wContractForm.btn_openList.clicked.connect(openItemslist)
    wContractForm.btn_delete.clicked.connect(remove_item)

    ### Shortcuts ###
    shrtClients = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+d'), wContractForm)  # Create the shortcut
    shrtClients.activated.connect(shortcut_used)  # Connect the shortcut
    ### Shortcuts ###

    wContractForm.show()


def form_load_customers(customers):
    tbl_customers.setColumnHidden(0, True)
    tbl_items.setColumnHidden(0, True)
    tbl_customers.horizontalHeader().setSectionResizeMode(1)
    tbl_items.horizontalHeader().setSectionResizeMode(1)

    for row_number, customer in enumerate(customers):
        tbl_customers.insertRow(row_number)
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))
            tbl_customers.setItem(row_number, column_number, cell)


def filter_list_clients():
    search_client = [
        (wContractForm.lbl_name.text()).lower(),
        (wContractForm.lbl_firstname.text()).lower(),
        (wContractForm.lbl_address.text()).lower(),
        (wContractForm.lbl_npa.text()).lower(),
        (wContractForm.lbl_town.text()).lower(),
        (wContractForm.lbl_phonefix.text()).lower(),
        (wContractForm.lbl_email.text()).lower(),
        (wContractForm.lbl_phone.text()).lower()
    ]
    match = False
    found_client = []

    for x in range(tbl_customers.rowCount()):
        for y in range(tbl_customers.columnCount()):
            if y > 0:
                found_client.append((tbl_customers.item(x, y).text()).lower())

        for f in range(len(search_client)):
            if found_client[f].find(search_client[f]) != -1:
                match = True
            else:
                match = False

                break

        tbl_customers.setRowHidden(x, not match)
        found_client.clear()


def shortcut_used():
    if tbl_customers.item(tbl_customers.currentRow(), 0) is not None:
        load_customer()


def load_customer():
    clicked_id = tbl_customers.item(tbl_customers.currentRow(), 0).text()

    customer = Customer()
    customer.load(clicked_id)

    wContractForm.lbl_name.setText(str(customer.lastname))
    wContractForm.lbl_firstname.setText(str(customer.firstname))
    wContractForm.lbl_address.setText(str(customer.address))
    wContractForm.lbl_npa.setText(str(customer.npa))
    wContractForm.lbl_town.setText(str(customer.town))
    wContractForm.lbl_phonefix.setText(str(customer.phone))
    wContractForm.lbl_phone.setText(str(customer.mobile))
    wContractForm.lbl_email.setText(str(customer.email))

    wContractForm.lbl_name.setReadOnly(True)
    wContractForm.lbl_firstname.setReadOnly(True)
    wContractForm.lbl_name.setStyleSheet("QLineEdit"
                                         "{"
                                         "background-color : rgba(0,0,0,0);"
                                         "border: 0px"
                                         "}")
    wContractForm.lbl_firstname.setStyleSheet("QLineEdit"
                                              "{"
                                              "background-color : rgba(0,0,0,0);"
                                              "border: 0px"
                                              "}")

    tbl_customers.setHidden(True)
    tbl_items.setHidden(False)
    wContractForm.label_21.setHidden(False)
    wContractForm.btn_openList.setHidden(False)
    wContractForm.btn_delete.setHidden(False)


    openItemslist()


def openItemslist():
    global wlistItems
    global table_items

    wlistItems = uic.loadUi('views/contract_items.ui')
    table_items = wlistItems.tbl_items

    form_load_items(Item.allWithColumns("items.id, itemnb, brand, model, stock"))

    wlistItems.lbl_serial.textChanged.connect(filter_list_items)
    table_items.cellClicked.connect(load_item_info)
    wlistItems.btn_pushRight.setDisabled(True)
    wlistItems.btn_pushRight.clicked.connect(add_item)
    wlistItems.btn_clear.clicked.connect(reset_form)

    table_items.horizontalHeader().setSectionResizeMode(1)

    wlistItems.move(0, 0)

    wlistItems.show()


def form_load_items(list_items):    
    durations_list = Duration.all()
    states_list = State.all()

    table_items.setColumnHidden(0, True)

    for row_number, items in enumerate(list_items):
        table_items.insertRow(row_number)

        for column_number, data in enumerate(items):
            cell = QtWidgets.QTableWidgetItem(str(data))
            table_items.setItem(row_number, column_number, cell)

    for st in states_list:
        wlistItems.drp_state.addItem(st[2])
    for t in durations_list:
        wlistItems.drp_time.addItem(t[2])

    wlistItems.drp_time.setCurrentIndex(len(durations_list) - 1)

    table_items.sortItems(1)


def filter_list_items():
    itemNb = (wlistItems.lbl_serial.text()).lower()

    for x in range(table_items.rowCount()):
        match = False
        found_item = (table_items.item(x, 1).text()).lower()

        if found_item.find(itemNb) != -1:
            match = True

        table_items.setRowHidden(x, not match)


def load_item_info():
    global item
    wlistItems.drp_time.currentIndexChanged.connect(load_price)
    wlistItems.drp_state.currentIndexChanged.connect(load_price)
    
    clicked_id = table_items.item(table_items.currentRow(), 0).text()

    item = Item()
    item.load(clicked_id)

    wlistItems.drp_state.setCurrentIndex(item.gear_state_id - 1)
    wlistItems.lbl_serial.setText(str(item.itemnb))
    wlistItems.lbl_brand.setText(str(item.brand))
    wlistItems.lbl_model.setText(str(item.model))
    wlistItems.lbl_stock.setText(str(item.stock))
    wlistItems.lbl_code.setText(str(item.article_number))

    wlistItems.btn_pushRight.setDisabled(False)
    wlistItems.lbl_serial.setReadOnly(True)
    wlistItems.lbl_serial.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")

def load_price():
    tst_duration = wlistItems.drp_time.currentIndex() + 1
    tst_state = wlistItems.drp_state.currentIndex() + 1

    price = item.get_location_price(tst_state, tst_duration)

    if price:
        wlistItems.lbl_price.setValue(float(price[0][4]))
    else:
        wlistItems.lbl_price.setValue(float(0))

def add_item():
    description = wlistItems.lbl_brand.text() + " " + wlistItems.lbl_model.text() + " " + str(
        item.size) + " (" + wlistItems.lbl_code.text() + ")"
    
    chosen_item = [
        str(item.id),
        wlistItems.lbl_serial.text(),
        description,
        wlistItems.drp_time.currentText(),
        wlistItems.drp_state.currentText(),
        str(wlistItems.lbl_price.value())
    ]

    currentRowCount = tbl_items.rowCount()
    tbl_items.insertRow(currentRowCount)

    for column_number in range(tbl_items.columnCount()):
        cell = QtWidgets.QTableWidgetItem(chosen_item[column_number])
        tbl_items.setItem(currentRowCount, column_number, cell)

    getTotal()
    save_item_state()
    reset_form()

def reset_form():
    wlistItems.drp_state.setCurrentIndex(0)
    wlistItems.lbl_serial.setText("")
    wlistItems.lbl_brand.setText("")
    wlistItems.lbl_model.setText("")
    wlistItems.lbl_stock.setText("")
    wlistItems.lbl_code.setText("")
    wlistItems.lbl_price.setValue(float(0))

    wlistItems.btn_pushRight.setDisabled(True)
    wlistItems.lbl_serial.setReadOnly(False)
    wlistItems.lbl_serial.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")

def getTotal():
    total_price = 0.00

    for row in range(tbl_items.rowCount()):
        total_price += float(tbl_items.item(row, 5).text())
    
    wContractForm.lbl_price.setText('Prix: CHF ' + str(total_price))

def remove_item():
    if(tbl_items.item(tbl_items.currentRow(), 0) != None):
        tbl_items.removeRow(tbl_items.currentRow())
        getTotal()

def save_item_state():
    actual_state = wlistItems.drp_state.currentIndex() + 1
    
    test_list = []

    if item.gear_state_id is not actual_state:
        item.gear_state_id = actual_state
        
        for attr, value in item.__dict__.items():
            #print(attr, value)
            if value is None:
                test_list.append("null")
            else:
                test_list.append(value)
        
        result = item.save(test_list[1:-1])