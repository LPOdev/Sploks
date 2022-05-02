from PyQt5 import QtWidgets, uic
from const import con
import sys

from model.staff import Staff

def displayStaffs():
    """
    Loads the staff_list.ui file and displays it
    """
    global wStaff
    wStaff = uic.loadUi('views/staff_list.ui')  # Load the .ui file
    loadData()
    wStaff.show()


def loadData():
    """
    It loads all the staffs from the database and insert them into the table
    """
    staffs = Staff.all()
    for row_number, staff in enumerate(staffs):
        wStaff.tableStaff.insertRow(row_number)
        for column_number, data in enumerate(staff):
            cell = QtWidgets.QTableWidgetItem(str(data))
            wStaff.tableStaff.setItem(row_number, column_number, cell)


