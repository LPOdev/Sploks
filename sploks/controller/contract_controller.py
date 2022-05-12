from PyQt5 import QtWidgets, QtGui, uic

from model.contract import Contract
from model.customer import Customer
from model.item import Item
from model.state import State


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
    shrtClients = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+d'), wContractForm)  # Create the shortcut
    shrtClients.activated.connect(shortcut_used)  # Connect the shortcut
    ### Shortcuts ###

    wContractForm.show()


def form_load_customers(customers):
    tbl_customers.setColumnHidden(0, True)
    tbl_customers.horizontalHeader().setSectionResizeMode(1)
    tbl_items.horizontalHeader().setSectionResizeMode(1)

    for row_number, customer in enumerate(customers):
        tbl_customers.insertRow(row_number)
        for column_number, data in enumerate(customer):
            cell = QtWidgets.QTableWidgetItem(str(data))
            tbl_customers.setItem(row_number, column_number, cell)


def filter_list():
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

    openItemslist()


def openItemslist():
    global wlistItems
    global table_items

    wlistItems = uic.loadUi('views/contract_items.ui')
    table_items = wlistItems.tbl_items

    form_load_items(Item.allWithColumns("items.id, itemnb, brand, model, stock"))

    wlistItems.lbl_serial.textChanged.connect(filter_list_items)
    table_items.cellClicked.connect(load_item_info)
    wlistItems.btn_pushRight.clicked.connect(add_item)

    table_items.horizontalHeader().setSectionResizeMode(1)

    wlistItems.show()


def form_load_items(list_items):
    global durations
    global items_price

    items_price = 0.00
    durations = [
        "J - Journée",
        "J2 - 2 Jours",
        "S - Semaine",
        "W - Weekend",
        "Z - Saison"
    ]

    table_items.setColumnHidden(0, True)

    for row_number, items in enumerate(list_items):
        table_items.insertRow(row_number)

        for column_number, data in enumerate(items):
            cell = QtWidgets.QTableWidgetItem(str(data))
            table_items.setItem(row_number, column_number, cell)

    for st in State.all():
        wlistItems.drp_state.addItem(st[2])

    for t in durations:
        wlistItems.drp_time.addItem(t)

    wlistItems.drp_time.setCurrentIndex(len(durations) - 1)
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

    clicked_id = table_items.item(table_items.currentRow(), 0).text()

    item = Item()
    item.load(clicked_id)

    wlistItems.drp_state.setCurrentIndex(item.gear_state_id - 1)

    wlistItems.lbl_serial.setText(str(item.itemnb))
    wlistItems.lbl_brand.setText(str(item.brand))
    wlistItems.lbl_model.setText(str(item.model))
    wlistItems.lbl_stock.setText(str(item.stock))
    wlistItems.lbl_code.setText(str(item.article_number))

    if item.cost is None:
        wlistItems.lbl_price.setValue(float(0))
    else:
        wlistItems.lbl_price.setValue(float(item.cost))


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

    table_items.removeRow(table_items.currentRow())

    add_price(wlistItems.lbl_price.value())
    reset_form()


def reset_form():
    wlistItems.drp_state.setCurrentIndex(0)
    wlistItems.lbl_serial.setText("")
    wlistItems.lbl_brand.setText("")
    wlistItems.lbl_model.setText("")
    wlistItems.lbl_stock.setText("")
    wlistItems.lbl_code.setText("")
    wlistItems.lbl_price.setValue(float(0))


def add_price(price):
    global items_price
    items_price += float(price)
    wContractForm.lbl_price.setText('Prix: CHF ' + str(items_price))
