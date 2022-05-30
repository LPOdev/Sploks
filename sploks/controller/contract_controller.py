from datetime import datetime
from PyQt5 import QtWidgets, QtGui,uic
import locale
locale.setlocale(locale.LC_TIME, "fr_FR") # Français

# reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas

import os

from model.contract import Contract
from model.customer import Customer
from model.helpers import Helpers
from model.item import Item
from model.state import State
from model.duration import Duration
from model.staff import Staff


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
    print("TBD")
    # global w_contract_details
    # global contract

    # contract = Contract()
    # contract.load(contract_id)

    # w_contract_details = uic.loadUi('views/contract_inspector.ui')

    # insertDetails()
    # w_contract_details.setWindowTitle(
    #     f"Contrat {contract.id} du {contract.creation_date} avec {contract.firstname} {contract.lastname}")
    # w_contract_details.show()


def insertDetails():
    """
    It takes the contract object and displays its details in the contract details window
    """
    print("TBD")
    # w_contract_details.lbl_id.setText(str(contract.id))
    # w_contract_details.lbl_creationDate.setText(contract.creation_date)
    # w_contract_details.lbl_returnDate.setText(contract.effective_return)
    # w_contract_details.lst_lastname.addItem(contract.lastname)
    # w_contract_details.lst_firstname.addItem(contract.firstname)
    # w_contract_details.lst_phone.addItem(contract.phone)
    # w_contract_details.lst_address.addItem(contract.address)
    # w_contract_details.lst_town.addItem(contract.town)
    # w_contract_details.lst_mobile.addItem(contract.mobile)
    # w_contract_details.lst_email.addItem(contract.email)

########## - Contract Form - ##########

def displayForm():
    global wContractForm
    global tbl_customers
    global tbl_items
    global total_price

    total_price = 0.00
    wContractForm = uic.loadUi('views/contract_form.ui')

    tbl_customers = wContractForm.customers_table
    tbl_items = wContractForm.equipement_table
    form_load_customers(Customer.all())

    # Hide Item Form
    tbl_items.setHidden(True)
    wContractForm.label_21.setHidden(True)
    wContractForm.btn_openList.setHidden(True)
    wContractForm.btn_delete.setHidden(True)
    wContractForm.btn_lock.setHidden(True)

    # Hide footer
    wContractForm.label_22.setHidden(True)
    wContractForm.label_23.setHidden(True)
    wContractForm.label_24.setHidden(True)
    wContractForm.label_25.setHidden(True)
    wContractForm.label_26.setHidden(True)
    wContractForm.date_toreturn.setHidden(True)
    wContractForm.date_paid.setHidden(True)
    wContractForm.date_taken.setHidden(True)
    wContractForm.drp_service.setHidden(True)
    wContractForm.drp_tune.setHidden(True)
    wContractForm.chk_notPaid.setHidden(True)
    wContractForm.chk_notTaken.setHidden(True)
    wContractForm.label_27.setHidden(True)
    wContractForm.txt_notes.setHidden(True)
    wContractForm.btn_send.setHidden(True)
    wContractForm.btn_print.setHidden(True)

    today = datetime.today()
    wContractForm.date_toreturn.setMinimumDateTime(today)
    wContractForm.date_taken.setMinimumDateTime(today)
    wContractForm.date_paid.setMinimumDateTime(today)

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
    wContractForm.btn_lock.clicked.connect(lock_items_table)
    wContractForm.btn_send.clicked.connect(send_contract)
    wContractForm.btn_print.clicked.connect(print_contract)   

    form_load_staff(Staff.all())

    ### Shortcuts ###
    shrtClients = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+d'), wContractForm)  # Create the shortcut
    shrtClients.activated.connect(shortcut_used)  # Connect the shortcut
    ### Shortcuts ###

    wContractForm.show()

def form_load_staff(list_staff):
    
    for staff in list_staff:
        wContractForm.drp_service.addItem(staff[0]+" "+staff[1])
        wContractForm.drp_tune.addItem(staff[0]+" "+staff[1])

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
    global customer
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
    wContractForm.btn_lock.setHidden(False)


    openItemslist()


def openItemslist():
    global wlistItems
    global table_items

    wlistItems = uic.loadUi('views/contract_items.ui')
    table_items = wlistItems.tbl_items

    form_load_items(Item.allWithColumns("items.id, itemnb, brand, model, stock","WHERE items.gearstate_id != 1"))

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
    global total_price
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

def lock_items_table():
    wlistItems.close()

    button_status = wContractForm.btn_openList.isEnabled()

    if button_status:
        wContractForm.btn_lock.setIcon(QtGui.QIcon("views/res/lock_icon.png"))

        # Show footer
        wContractForm.label_22.setHidden(False)
        wContractForm.label_23.setHidden(False)
        wContractForm.label_24.setHidden(False)
        wContractForm.label_25.setHidden(False)
        wContractForm.label_26.setHidden(False)
        wContractForm.date_toreturn.setHidden(False)
        wContractForm.date_paid.setHidden(False)
        wContractForm.date_taken.setHidden(False)
        wContractForm.drp_service.setHidden(False)
        wContractForm.drp_tune.setHidden(False)
        wContractForm.chk_notPaid.setHidden(False)
        wContractForm.chk_notTaken.setHidden(False)
        wContractForm.label_27.setHidden(False)
        wContractForm.txt_notes.setHidden(False)
        wContractForm.btn_send.setHidden(False)

    else:
        wContractForm.btn_lock.setIcon(QtGui.QIcon("views/res/unlock_icon.png"))

        # Hide footer
        wContractForm.label_22.setHidden(True)
        wContractForm.label_23.setHidden(True)
        wContractForm.label_24.setHidden(True)
        wContractForm.label_25.setHidden(True)
        wContractForm.label_26.setHidden(True)
        wContractForm.date_toreturn.setHidden(True)
        wContractForm.date_paid.setHidden(True)
        wContractForm.date_taken.setHidden(True)
        wContractForm.drp_service.setHidden(True)
        wContractForm.drp_tune.setHidden(True)
        wContractForm.chk_notPaid.setHidden(True)
        wContractForm.chk_notTaken.setHidden(True)
        wContractForm.label_27.setHidden(True)
        wContractForm.txt_notes.setHidden(True)
        wContractForm.btn_send.setHidden(True)
    
    wContractForm.btn_openList.setEnabled(not button_status)
    
def send_contract():
    lock_form()
    new_contract = Contract()
    my_sql_date = "%Y-%m-%d %H:%M:%S"
    date_format_string = "dd.MM.yyyy"

    return_date = f"{Helpers.dateToSQL((wContractForm.date_toreturn.dateTime()).toString(date_format_string))}"
    today = f"{(datetime.today()).strftime(my_sql_date)}"

    if wContractForm.chk_notPaid.checkState():
        paid_on = None
    else:
        paid_on = f"{Helpers.dateToSQL((wContractForm.date_paid.dateTime()).toString(date_format_string))}"

    if wContractForm.chk_notTaken.checkState():
        take_on = None
    else:
        take_on = f"{Helpers.dateToSQL((wContractForm.date_taken.dateTime()).toString(date_format_string))}"

    if wContractForm.txt_notes.toPlainText() == "":
        notes = None
    else:
        notes = wContractForm.txt_notes.toPlainText()
    
    new_contract_informations = (
        today,
        return_date,
        customer.id,
        notes,
        total_price,
        take_on,
        paid_on,
        wContractForm.drp_service.currentIndex() + 1,
        wContractForm.drp_tune.currentIndex() + 1,
    )

    new_contract.create(new_contract_informations)

    rent_items(new_contract, wContractForm.drp_service.currentText(), wContractForm.drp_tune.currentText())

    wContractForm.btn_print.setHidden(False)

def rent_items(contract, help_staff, tune_staff):
    chosen_items = []

    for row in range(tbl_items.rowCount()):
        row_items = [row+1]
        
        for col in range(tbl_items.columnCount()):
            tst_item = tbl_items.item(row, col).text()
            row_items.append(tst_item)

        chosen_items.append(row_items)

    items_toPrint = []
    for x in range(len(chosen_items)):
        item.load(chosen_items[x][1])
        
        rented_item = (
            item.id,
            contract.id,
            Duration.findId(chosen_items[x][4])['id'],
            item.gear_state_id,
            chosen_items[x][6],
            chosen_items[x][3],
            chosen_items[x][0],
            0
        )
        
        Item.save_rented(rented_item)

        items_toPrint.append([chosen_items[x][2], chosen_items[x][3], item.geartype_id, chosen_items[x][4], chosen_items[x][6]])

    global to_print
    to_print = [
        contract.id,
        customer.lastname,
        customer.firstname,
        customer.address,
        customer.npa,
        customer.town,
        customer.mobile,
        customer.phone,
        customer.email,
        contract.planned_return,
        contract.creation_date,
        contract.total,
        contract.takenon,
        contract.paidon,
        contract.notes,
        help_staff,
        tune_staff,
        items_toPrint
    ]

def lock_form():
    readonly_style = "QLineEdit{background-color : rgba(0,0,0,0);border: 0px}"

    if wContractForm.chk_notPaid.checkState():
        wContractForm.chk_notPaid.setEnabled(False)
        wContractForm.date_paid.setHidden(True)
        
    else:
        wContractForm.chk_notPaid.setHidden(True)
        wContractForm.date_paid.setReadOnly(True)


    if wContractForm.chk_notTaken.checkState():
        wContractForm.chk_notTaken.setEnabled(False)
        wContractForm.date_taken.setHidden(True)

    else:
        wContractForm.chk_notTaken.setHidden(True)
        wContractForm.date_taken.setReadOnly(True)

    # Buttons & checkboxes
    wContractForm.btn_send.setHidden(True)
    wContractForm.btn_lock.setEnabled(False)
    wContractForm.btn_delete.setEnabled(False)
    
    # Dropboxes
    wContractForm.drp_service.setEnabled(False)
    wContractForm.drp_tune.setEnabled(False)
    
    # DateEdits
    wContractForm.date_toreturn.setReadOnly(True)
    
    # Client informations
    wContractForm.lbl_phone.setReadOnly(True)
    wContractForm.lbl_phonefix.setReadOnly(True)
    wContractForm.lbl_address.setReadOnly(True)
    wContractForm.lbl_email.setReadOnly(True)
    wContractForm.lbl_town.setReadOnly(True)
    wContractForm.lbl_npa.setReadOnly(True)
    wContractForm.txt_notes.setReadOnly(True)

    wContractForm.lbl_phone.setStyleSheet(readonly_style)
    wContractForm.lbl_phonefix.setStyleSheet(readonly_style)
    wContractForm.lbl_address.setStyleSheet(readonly_style)
    wContractForm.lbl_email.setStyleSheet(readonly_style)
    wContractForm.lbl_town.setStyleSheet(readonly_style)
    wContractForm.lbl_npa.setStyleSheet(readonly_style)
    wContractForm.txt_notes.setStyleSheet("QTextEdit{background-color: rgba(0, 0, 0, 0);}")

def print_contract():
    
    width,height = A4
    logo = "logo-sports-time.png"
    title = "contrat.pdf"

    nb_contrat = to_print[0]
    nom = to_print[1]
    firstname = to_print[2]
    address = to_print[3]
    npa = to_print[4]
    town = to_print[5]
    phone = to_print[6]
    phonefix = to_print[7]
    email = to_print[8]
    retour = to_print[9]
    today = to_print[10]
    total = to_print[11]
    takeon = to_print[12]
    paidon = to_print[13]
    notes = to_print[14]
    service = to_print[15]
    tune = to_print[16]
    loc_items = to_print[17]

    doc = canvas.Canvas("contrat.pdf", pagesize = A4)
    doc.setTitle(f"Contrat {nb_contrat}")
    doc.setLineWidth(.3)

    doc.drawInlineImage(logo, width/6, 650, 6*inch, 2*inch)

    doc.setFont('Helvetica-Bold', 15)
    doc.drawString(30, 620, f"Contrat de location {nb_contrat}")

    ##### - CLIENT INFORMATION - #####
    doc.setFont('Helvetica-Bold', 12)
    doc.drawString(30, 580, f"Nom: {nom}")
    doc.line(65, 578, 345, 578)

    doc.drawString(350, 580, f"Prénom: {firstname}")
    doc.line(400, 578, 550, 578)

    doc.drawString(30, 560, f"Adresse: {address}")
    doc.line(85, 558, 550, 558)

    doc.drawString(30, 540, f"Ville: {town}")
    doc.line(60, 538, 345, 538)

    doc.drawString(350, 540, f"Code postal: {npa}")
    doc.line(425, 538, 550, 538)

    doc.drawString(30, 520, f"Tél: {phonefix}")
    doc.line(55, 518, 345, 518)

    doc.drawString(350, 520, f"Natel: {phone}")
    doc.line(385, 518, 550, 518)

    doc.drawString(30, 500, f"Email: {email}")
    doc.line(70, 498, 550, 498)

    ##### - DATES - #####
    doc.drawString(30, 480, f"Date de location: {today}")
    #doc.line(130, 478, 345, 478)

    doc.drawString(350, 480, f"Date de retour: {retour}")
    #doc.line(120, 458, 345, 458)

    ##### - ITEMS - #####
    doc.setFont('Helvetica', 10)

    # TABLE HEADERS
    doc.drawString(50, 450, "No")
    doc.drawString(150, 450, "Objet")
    doc.drawString(350, 450, "Cat")
    doc.drawString(390, 450, "Durée")
    doc.drawString(520, 450, "Montant")
    row_height = 435

    # TABLE CONTENT
    for i in range(len(loc_items)):
        doc.drawString(30, row_height, f"{i+1}")

        doc.drawString(50, row_height, f"{loc_items[i][0]}")
        doc.drawString(150, row_height, f"{loc_items[i][1]}")
        doc.drawString(350, row_height, f"{loc_items[i][2]}")
        doc.drawString(390, row_height, f"{loc_items[i][3]}")
        doc.drawString(510, row_height, f"SFr. {loc_items[i][4]}")
        
        row_height -= 15

    ##### - Contract info - #####
    h = row_height - 50

    doc.setFont('Helvetica-Bold', 18)
    doc.drawString(400, h, f"Total: SFr. {total}")

    doc.setFont('Helvetica', 10)
    doc.drawString(30, h, f"Payé le {paidon}")
    doc.drawString(200, h, f"Pris le {takeon}")

    doc.drawString(30, h-20, f"Servi par {service}")
    doc.drawString(200, h-20, f"Matériel réglé par {tune}")

    doc.drawString(200, h-20, f"Matériel réglé par {tune}")

    doc.drawString(300, h-60, "Signature du client:")
    doc.line(300, h-62, 550, h-62)

    doc.drawString(30, h-90, "Notes diverses:")
    doc.drawString(40, h-105, f"{notes}")

    hauteur = 150

    message_style = ParagraphStyle('Normal')

    with open('rights.txt') as f:
        for line in f:
            message = line.replace('\n', '<br />')
            message = Paragraph((message).encode('latin1'), message_style)
            w, h = message.wrap(500, 15)
            message.drawOn(doc, 30, hauteur - h)
            hauteur -= h



    doc.drawString(width/6, 600, "Le matériel doit être rendu propre, une surtaxe de Frs 10.- peut être demandée")

    doc.save()

    os.startfile("contrat.pdf")