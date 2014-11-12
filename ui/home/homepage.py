################################################################################
# Home page.

################################################################################
# Import Statements.
import sys

from PyQt4 import QtGui, QtCore

from core.repository import MovieRepository
from core.repository import Wait
from core.utils import StringUtils

from core.domainobjects import MovieModel
import core.Constants as Constants

from ui.home.MovieTable import MovieTable
from ui.home.AddMovieRequest import AddMovieRequest

import ui.DefaultComponents

################################################################################
# Global Declarations
mdb = MovieRepository()

################################################################################
class MovieManager(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MovieManager, self).__init__(parent)
        
        self.createWidget()
        
        self.statusBar().showMessage("Manage Movies Collection", 100000)

        self.setWindowTitle("Chiya(Paridhi) also Called Puiyan | Ki Dukan")
        self.setGeometry(200, 500,500,500)
        
        self.setWindowIcon(QtGui.QIcon("icons/windowicon.png"))
        
    def createWidget(self):
        #central view
        self.centerContainer = CentralWidget(self)

        #add toolbar
        MovieManagerToolBar().create(self)
        
    def refreshTableView(self, movies=[]):
        self.centerContainer.refresh(movies)
        
    def addNewRequestClicked(self):
        self.centerContainer.addNewRequestClicked()

    def showSearchWidget(self):
        self.centerContainer.showSearchWidget()
    
    def updateView(self, movieModel):        
        self.centerContainer.updateView(movieModel)    
        
    def show_view(self):
        self.show()

################################################################################
class CentralWidget(QtGui.QWidget):
    
    def __init__(self, mainWindow):
        super(CentralWidget, self).__init__()
        
        self.create(mainWindow)
        
        
    def create(self, mainWindow):

        self.movieTable = MovieTable(mainWindow)
        
        #add data to movie table
        movies = mdb.loadAllMovies()
        self.refresh(movies)

        vbox = QtGui.QVBoxLayout()
        
        self.searchWidget = SearchWidget(mainWindow)
        vbox.addWidget(self.searchWidget)
        
        vbox.addWidget(self.movieTable)
                
        hbox = QtGui.QHBoxLayout()
        
        #widget to add and update movies
        self.addMovieRequest = AddMovieRequest(mainWindow)
        hbox.addWidget(self.addMovieRequest) 
        self.addMovieRequest.hide()

        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        mainWindow.setCentralWidget(self)
    
    def addNewRequestClicked(self):
        self.addMovieRequest.showAddView()
        
    def updateView(self, movieModel):
        self.addMovieRequest.showUpdateView(movieModel)
        
    def refresh(self, movies = []):
        self.movieTable.updateData(movies)

    def showSearchWidget(self):
        self.searchWidget.showView()
        
    def searchForMovie(self):
        self.centerContainer
        print "search clicked"

################################################################################
class MovieManagerToolBar:

    def create(self, mainWindow):
        toolbar =  mainWindow.addToolBar("Home Tools")
        toolbar.setStyleSheet("border:1;"
                             "color : black;")
        # Add New Request 
        newRequest = QtGui.QAction(QtGui.QIcon("icons/addmovie.png"), 
                                    "Add New Request", toolbar)
        newRequest.setShortcut("Ctrl+N")
        newRequest.setStatusTip("Add new Movie")
        mainWindow.connect(newRequest, QtCore.SIGNAL('triggered()'), 
                                                mainWindow.addNewRequestClicked)
        toolbar.addAction(newRequest)

        #search box
        search = QtGui.QAction(QtGui.QIcon("icons/search.png"), 
                                            "Search by Name", toolbar)
        search.setShortcut("Ctrl+F")
        search.setStatusTip("Search for Movie")
        mainWindow.connect(search, QtCore.SIGNAL("triggered()"),
                                                    mainWindow.showSearchWidget)
        toolbar.addAction(search)
        
        # Add Separator
        toolbar.addSeparator()

        #exit action
        exit = QtGui.QAction(QtGui.QIcon("icons/exit.png"), "Exit", toolbar)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip("Exit application")
        mainWindow.connect(exit, QtCore.SIGNAL("triggered()"), 
                                                QtCore.SLOT("close()"))
        toolbar.addAction(exit)
        
        #prepare menubar
        menubar = mainWindow.menuBar()
        fileMenu = menubar.addMenu("&Manager")
        fileMenu.addAction(newRequest)
        fileMenu.addSeparator()
        fileMenu.addAction(exit)
        
        searchMenu =  menubar.addMenu("&Search")         
        searchMenu.addAction(search)
        
################################################################################
class SearchWidget(QtGui.QFrame):
    
    def __init__(self, mainWindow):
        super(SearchWidget, self).__init__()
        
        self.mainWindow = mainWindow
        self.createWidget()
        self.setStyleSheet(Constants.WIDGET_STYLE_WITH_BORDER)

    
    def createWidget(self):
        hbox = QtGui.QHBoxLayout(self)
        hbox.addStretch(1)
        #create box
        self.searchBox = QtGui.QLineEdit(self)
        self.connect(self.searchBox, 
                    QtCore.SIGNAL("cursorPositionChanged (int,int)"), 
                    self.searchButtonClicked)
        self.searchBox.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        
        label = ui.DefaultComponents.SystemLabel(self, "Search By Movie Name")            

        searchButton = ui.DefaultComponents.SystemButton(self, " Search ")
        searchButton.connect(searchButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.searchButtonClicked)
        
        cancelButton = ui.DefaultComponents.SystemButton(self, " Cancel ")
        cancelButton.connect(cancelButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.cancelButtonClicked)
        
        hbox.addWidget(label)
        hbox.addWidget(self.searchBox, 2)
        hbox.addWidget(searchButton, 1)
        hbox.addWidget(cancelButton, 1)
        
        self.setLayout(hbox)
        
        self.hide()
            
    def showView(self):
        self.show()
        self.searchBox.clear()
        
    def searchButtonClicked(self):
        nameToSearch = self.searchBox.text()
        movies = mdb.findMatchingMovies(str(nameToSearch))
        self.mainWindow.refreshTableView(movies)
    
    def cancelButtonClicked(self):
        self.hide()
        movies = mdb.loadAllMovies()
        self.mainWindow.refreshTableView(movies)

    def updateCurrentIndexFor(self, itemText):
        index = self.findText(itemText)
        self.setCurrentIndex(index)
################################################################################        
