
from PyQt4 import QtGui, QtCore

from core.repository import MovieRepository
import core.Constants as Constants


class MovieTable(QtGui.QTableWidget):
    
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        super(MovieTable, self).__init__()    
        
        #Init database
        self.movieRepository = MovieRepository()
        
        self.addHeaders()

        #set column width
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 250)
        self.setColumnWidth(3, 150)                                        
        self.setWordWrap(True)
        self.setAlternatingRowColors(True)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        self.setStyleSheet(Constants.WIDGET_STYLE_WITH_BORDER)

        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        
        self.connect(self, QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.rowClicked)
      
    def addHeaders(self):
        #Add Headers to table
        headers = ["ID","Name","Spoken Language", "Status","Storage","Comments"]

        for columnId, header in enumerate(headers):
            self.insertColumn(columnId) 
            headerItem = QtGui.QTableWidgetItem(header)
            self.setHorizontalHeaderItem(columnId, headerItem)

        self.verticalHeader().setVisible(False)
        
    def updateData(self, movies):
        
        #Clear Old Data.
        self.clearContents()
        
        self.setRowCount(len(movies))

        #Add Data to this table
        for i in range(len(movies)):
            movie = movies[i]
            
            self.createTableCell(i, 0, movie._id)
            self.createTableCell(i, 1, movie.name)
            self.createTableCell(i, 2, movie.spokenLanguage)        
            self.createTableCell(i, 3, movie.status)
            self.createTableCell(i, 4, movie.storage)
            self.createTableCell(i, 5, movie.comments)        
    
    def createTableCell(self, row, column, cellData, editable = False):
        cell = QtGui.QTableWidgetItem(str(cellData), 
                                      QtGui.QTableWidgetItem.UserType)
        if not editable:
            cell.setFlags(QtCore.Qt.ItemFlags(QtCore.Qt.ItemIsEnabled |
                                                QtCore.Qt.ItemIsSelectable))
            
        self.setItem(row, column, cell);
    
    def rowClicked(self, row, column):
        #Name for the movie selected in the table
        nameItem = self.item(row, 1).text()
        movieModel = self.movieRepository.findMovieByName(str(nameItem))
        self.mainWindow.updateView(movieModel);

