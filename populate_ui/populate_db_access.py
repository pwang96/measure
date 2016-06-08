__author__ = 'masslab'

from PyQt4 import QtGui, QtCore
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

environment_columns = ['ID',
                       'Model',
                       'Serial',
                       'Probe',
                       'Room',
                       'Coeff (a)',
                       'Coeff (b)',
                       'Coeff (c)',
                       'Uncertainty',
                       'Calibration Date',
                       'Baudrate',
                       'Parity',
                       'Bytesize'
                       'Stopbits',
                       'Timeout']

weights_columns = ['ID',
                   'Serial #',
                   'Name',
                   'Units',
                   'Nominal',
                   'Customer Name',
                   'Density',
                   'Density Uncertainty',
                   'Volumetric Expansion',
                   'Comments']


def populate_db_access(cls, table):

    data_table = cls.db.populate_db_access(table)
    cls.ui.dbTable.clear()

    if table in ('thermometers', 'hygrometers', 'barometers'):
        cls.ui.dbTable.setColumnCount(len(environment_columns))
        cls.ui.dbTable.setHorizontalHeaderLabels(environment_columns)

    else:
        cls.ui.dbTable.setColumnCount(len(weights_columns))
        cls.ui.dbTable.setHorizontalHeaderLabels(weights_columns)

    rows = len(data_table[0])

    cls.ui.dbTable.setRowCount(rows)

    # Go row by row and then column by column to fill in the items
    for rowcount in range(rows):

        for colcount in range(int(cls.ui.dbTable.columnCount())):
            item = QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str(data_table[rowcount][colcount])))
            cls.ui.dbTable.setItem(rowcount, colcount, item)
