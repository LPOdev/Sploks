from PyQt5 import QtWidgets, QtGui, QtCore,uic
from model.timerMessageBox import TimerMessageBox
from model.item import Item
from model.state import State
import controller.contract_controller as contractControler

tstEditMode = False


def displayStock():
    """
    Loads the item list view and displays it
    """
    global w_stock
    w_stock = uic.loadUi('views/item_list.ui')  # Load the .ui file
    loadItems(Item.all())
    w_stock.tableStock.horizontalHeader().setSectionResizeMode(1)
    w_stock.show()


def loadItems(stock):
    """
    It displays all the items in the table
    
    :param stock: The list of items to display
    """
    w_stock.tableStock.setColumnHidden(0, True)
    for row_number, stock in enumerate(stock):
        w_stock.tableStock.insertRow(row_number)

        for column_number, data in enumerate(stock):
            cell = QtWidgets.QTableWidgetItem(str(data))
            w_stock.tableStock.setItem(row_number, column_number, cell)

    w_stock.tableStock.cellClicked.connect(itemDetails)   

    ### Shortcuts ###
    shrtDetails = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+d'), w_stock)    # Create the shortcut
    shrtDetails.activated.connect(shortcut_used)   # Connect the shortcut
    ### Shortcuts ###

    w_stock.lblSearchBox.textChanged.connect(filter_list)

def filter_list():
    """
    The function iterates through each row of the table and checks if the text in any of the cells
    contains the filter text. 
    If it does, the row is shown. If it doesn't, the row is hidden
    """
    filter_txt = w_stock.lblSearchBox.text()
    # The above code is a loop that loops through the rows of the table.
    #         It then loops through the columns of the table.
    #         If the text of the cell contains the filter text, then the row is shown.
    #         Otherwise, the row is hidden.
    for x in range(w_stock.tableStock.rowCount()):
        match = False
        for y in range(w_stock.tableStock.columnCount()):
            found_item = w_stock.tableStock.item(x,y)
            txt = (found_item.text()).lower()
            if txt.find(filter_txt.lower()) != -1:
                match = True
                break
                
        w_stock.tableStock.setRowHidden(x, not match)

def shortcut_used():
    """
    If the user clicks on a row in the table, the item details are displayed
    """
    if(w_stock.tableStock.item(w_stock.tableStock.currentRow(), 0) != None):
        itemDetails()

def itemDetails():
    """
    Display the details of one item using it id
    """
    global w_item_details
    w_item_details = uic.loadUi('views/item_inspector.ui')

    item_id = w_stock.tableStock.item(w_stock.tableStock.currentRow(), 0).text()

    global item
    item = Item()
    item.load(item_id)

    global state
    state = State()
    state.load(item.gear_state_id)

    global state_list
    state_list = State.all()
    for st in state_list:
        w_item_details.drplstState.addItem(st[2])

    insertDetails()
    global contracts_list
    
    contracts_list = item.contracts()
    w_item_details.lbl_nbContracts.setText(str(len(contracts_list)))

    if len(contracts_list) < 1:
        w_item_details.btnContracts.setDisabled(True)

    w_item_details.btnContracts.clicked.connect(itemContracts)
    w_item_details.btnEditCancel.clicked.connect(switchEditMode)
    w_item_details.btnSave.clicked.connect(saveItemModifications)

    w_item_details.show()


def switchEditMode():
    """
    This function is called when the user clicks the edit button.
    It changes the state of the GUI to edit mode.
    """
    global w_item_details
    global tstEditMode

    # Checking if the user is in edit mode. If they are, it will display the text.
    if tstEditMode is True:
        insertDetails()
        tstEditMode = False
        w_item_details.lblItemCode.setReadOnly(True)
        w_item_details.lblSize.setReadOnly(True)
        w_item_details.lblType.setReadOnly(True)
        w_item_details.lblBrand.setReadOnly(True)
        w_item_details.lblModel.setReadOnly(True)
        w_item_details.lblPrice.setReadOnly(True)
        w_item_details.lblReturned.setReadOnly(True)
        w_item_details.lblSerialNumber.setReadOnly(True)
        w_item_details.lblStock.setReadOnly(True)

        # Set input style
        w_item_details.drplstState.setDisabled(True)
        w_item_details.btnSave.setDisabled(True)
        w_item_details.btnEditCancel.setIcon(QtGui.QIcon("views/res/edit_icon.png"))
        w_item_details.btnEditCancel.setIconSize(QtCore.QSize(30,30))
        w_item_details.lblItemCode.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblSize.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblType.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblBrand.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblModel.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblPrice.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblReturned.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblSerialNumber.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblStock.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")

    else:
        tstEditMode = True
        w_item_details.lblItemCode.setReadOnly(False)
        w_item_details.lblSize.setReadOnly(False)
        w_item_details.lblType.setReadOnly(False)
        w_item_details.lblBrand.setReadOnly(False)
        w_item_details.lblModel.setReadOnly(False)
        w_item_details.lblPrice.setReadOnly(False)
        w_item_details.lblReturned.setReadOnly(False)
        w_item_details.lblSerialNumber.setReadOnly(False)
        w_item_details.lblStock.setReadOnly(False)

        # Set input style
        w_item_details.drplstState.setDisabled(False)
        w_item_details.btnSave.setDisabled(False)
        w_item_details.btnEditCancel.setIcon(QtGui.QIcon("views/res/cancel_icon.png"))
        w_item_details.btnEditCancel.setIconSize(QtCore.QSize(30,30))
        w_item_details.lblItemCode.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblSize.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblType.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblBrand.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblModel.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblPrice.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblReturned.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblSerialNumber.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")
        w_item_details.lblStock.setStyleSheet("QLineEdit"
                        "{"
                        "background: white;"
                        "border: 1px solid gray"
                        "}")

def insertDetails():
    """
    The function inserts the item details in the window labels
    """
    w_item_details.lblItemCode.setText(item.article_number)
    w_item_details.lblSerialNumber.setText(item.itemnb)
    if item.cost == None:
        w_item_details.lblPrice.setText("0")
    else:
        w_item_details.lblPrice.setText(str(item.cost))
    w_item_details.lblReturned.setText(str(item.returned))
    w_item_details.lblBrand.setText(item.brand)
    w_item_details.lblModel.setText(item.model)
    w_item_details.lblType.setText(item.geartype)
    w_item_details.lblStock.setText(str(item.stock))
    w_item_details.lblSize.setText(str(item.size))
    w_item_details.drplstState.setCurrentIndex(item.gear_state_id - 1)

def itemContracts():
    """
    This function displays the contracts of one item
    """
    global w_item_contracts
    w_item_contracts = uic.loadUi('views/contracts_list.ui')
    loadContracts(contracts_list)
    w_item_contracts.setWindowTitle(f"Contrats de location de {item.brand} {item.model} {item.itemnb}")
    w_item_contracts.show()


def loadContracts(contracts):
    """
    This function displays all the contracts of an item
    
    :param contracts: The contracts of the item. Type: Array
    """
    w_item_contracts.tableContracts.setColumnCount(len(contracts[0]))

    for row_number, contracts in enumerate(contracts):
        w_item_contracts.tableContracts.insertRow(row_number)

        for column_number, data in enumerate(contracts):
            cell = QtWidgets.QTableWidgetItem(str(data))
            w_item_contracts.tableContracts.setItem(row_number, column_number, cell)

        # The above code is connecting the cellClicked signal of the tableWidget to the
        # loadContractDetails function.
        w_item_contracts.tableContracts.cellClicked.connect(loadContractDetails)


def loadContractDetails():
    """
    It loads the contract details for the selected contract
    """
    item_id = w_stock.tableStock.item(w_stock.tableStock.currentRow(), 0).text()
    contract_id = w_item_contracts.tableContracts.item(w_item_contracts.tableContracts.currentRow(), 0).text()
    contractControler.displayContractDetails(contract_id)

def saveItemModifications():
    """
    Save the item modifications
    """
    global tstEditMode

    # update item properties
    item.article_number = w_item_details.lblItemCode.text()
    item.itemnb = w_item_details.lblSerialNumber.text()
    item.cost = w_item_details.lblPrice.text()
    item.returned = w_item_details.lblReturned.text()
    item.brand = w_item_details.lblBrand.text()
    item.model = w_item_details.lblModel.text()
    item.geartype = w_item_details.lblType.text()
    item.stock = w_item_details.lblStock.text()
    item.size = w_item_details.lblSize.text()
    item.gear_state_id = w_item_details.drplstState.currentIndex() + 1
    
    # update item properties in the database
    save_problems = item.save([item.itemnb, item.brand, item.model, item.size, item.gear_state_id, item.cost, item.returned, item.stock, item.article_number, item.geartype_id])
    
    if save_problems == True:
        
        error_message = QtWidgets.QMessageBox()
        error_message.setIcon(QtWidgets.QMessageBox.Critical)
        error_message.setText("Problème à l'enregistrement des données")
        error_message.setInformativeText("Un problème est survenu lors de l'enregistrement de vos modifications. Les modifications n'ont pas étés enregistrées.")
        error_message.setWindowTitle("Erreur")
        error_message.exec_()
        
        item.load(item.id)

    else:
        # leave Edit mode
        tstEditMode = False
        w_item_details.lblItemCode.setReadOnly(True)
        w_item_details.lblSize.setReadOnly(True)
        w_item_details.lblType.setReadOnly(True)
        w_item_details.lblBrand.setReadOnly(True)
        w_item_details.lblModel.setReadOnly(True)
        w_item_details.lblPrice.setReadOnly(True)
        w_item_details.lblReturned.setReadOnly(True)
        w_item_details.lblSerialNumber.setReadOnly(True)
        w_item_details.lblStock.setReadOnly(True)

        # Set input style
        w_item_details.drplstState.setDisabled(True)
        w_item_details.btnSave.setDisabled(True)
        w_item_details.btnEditCancel.setIcon(QtGui.QIcon("views/res/edit_icon.png"))
        w_item_details.btnEditCancel.setIconSize(QtCore.QSize(30,30))
        w_item_details.lblItemCode.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblSize.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblType.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblBrand.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblModel.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblPrice.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblReturned.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblSerialNumber.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")
        w_item_details.lblStock.setStyleSheet("QLineEdit"
                        "{"
                        "background-color : rgba(0,0,0,0);"
                        "border: 0px"
                        "}")

        tmrMsg = TimerMessageBox(1, "Les modifications ont étés enregistrées.")
        tmrMsg.exec_()