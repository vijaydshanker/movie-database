from PyQt4 import QtGui, QtCore

from core.domainobjects import MovieModel
import core.Constants as Constants

import ui.DefaultComponents

SAVE_BUTTON_LABEL = " Save "
UPDATE_BUTTON_LABEL = " Update "

class AddMovieRequest(QtGui.QFrame):
  
    def __init__(self, mainWindow):
    
        super(AddMovieRequest, self).__init__()

        self.mainWindow = mainWindow
        
        self.setStyleSheet(Constants.WIDGET_STYLE_WITH_BORDER)
            
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        self.createWidget(False)
                
    def showUpdateView(self, movieModel):
        self.nameText.setText(movieModel.name)
        self.nameText.setReadOnly(True)

        self.spokenLanguageText.updateCurrentIndexFor(movieModel.spokenLanguage)
        self.statusText.updateCurrentIndexFor(movieModel.status)
        self.storageText.updateCurrentIndexFor(movieModel.storage)        
        
        self.commentsText.setDocument(QtGui.QTextDocument(movieModel.comments))
        self.okButton.setText(UPDATE_BUTTON_LABEL)
        
        self.show();
    
    def showAddView(self):
        self.clear()
        self.okButton.setText(SAVE_BUTTON_LABEL)
        self.show()
                
    def createWidget(self, withErrors):
        
        nameLabel = ui.DefaultComponents.SystemLabel(self,"Name")
        spokenLanguageLabel = ui.DefaultComponents.SystemLabel(self, "Spoken Language")
        statusLabel = ui.DefaultComponents.SystemLabel(self, "Status")
        storageLabel = ui.DefaultComponents.SystemLabel(self, "Storage")
        commentsLabel = ui.DefaultComponents.SystemLabel(self, "Comments")
        
        self.nameText = QtGui.QLineEdit()
        
        self.spokenLanguageText = PropertyComboBox(["Hindi", "English"])
        self.statusText = PropertyComboBox(["Downloaded", "Seen", "Not Downloaded", "Not Found", "Need To Purchage"])
        self.storageText = PropertyComboBox(["me@homework", "manu's laptop", "me@store", "maanu@store"])
        
        self.commentsText = QtGui.QTextEdit()
        
        row = 0
        column = 0;
        if(withErrors):
            pass
                        
        self.okButton = SaveButton(self)
        self.cancelButton = CancelButton(self)
        
        # Details of the movie
        movieDetailBox = QtGui.QGridLayout()
        movieDetailBox.setSpacing(5)
        movieDetailBox.addWidget(nameLabel, 0,0)
        movieDetailBox.addWidget(self.nameText,0,2)
        movieDetailBox.addWidget(statusLabel, 1, 0)
        movieDetailBox.addWidget(self.statusText,1, 2)
        movieDetailBox.addWidget(storageLabel, 2, 0)
        movieDetailBox.addWidget(self.storageText, 2, 2)
        movieDetailBox.addWidget(spokenLanguageLabel, 3, 0)
        movieDetailBox.addWidget(self.spokenLanguageText, 3, 2)
        
        # Comments
        commentsBox = QtGui.QGridLayout()
        commentsBox.addWidget(commentsLabel, 1, 4)
        commentsBox.addWidget(self.commentsText, 2, 4)
        
        # Buttons: Actions for this page.
        actionBox = QtGui.QHBoxLayout()
        actionBox.addWidget(self.okButton)
        actionBox.addStretch(2)
        actionBox.addWidget(self.cancelButton)
        
        mainGrid = QtGui.QGridLayout()

        mainGrid.addLayout(movieDetailBox, 1, 1)
        mainGrid.addLayout(commentsBox, 1, 2)
        mainGrid.addLayout(actionBox, 3, 1, 1, 2)                
        
        self.setLayout(mainGrid)
        
    def save(self):
    
        movieModel = self.bindModel();
        
        errors = movieModel.validate()
        if(len(errors) > 0):
            showErrors()
        else:
            # save movie to db
            MovieDatabase().addMovie(movieModel)
            
            #refresh the center view
            movies = MovieDatabase().loadAllMovies()
            self.mainWindow.refreshTableView(movies)            
            
            #Now remove
            self.cancel()
    
    def update(self):
        toUpdate = self.bindModel();
                
        errors = toUpdate.validate()
        if(len(errors) > 0):
            showErrors()
        else:
            moviedb = MovieDatabase()
            
            movieModel = moviedb.findByName(toUpdate.name)
            movieModel = movieModel.copyProperties(toUpdate, movieModel)  
                        
            # save movie to db
            moviedb.updateMovie(movieModel)
            
            #refresh the center view
            movies = MovieDatabase().loadAllMovies()
            self.mainWindow.refreshTableView(movies)            
            
            #Now remove
            self.cancel()
        
    def bindModel(self):

        movieModel = MovieModel()
        movieModel.name = str(self.nameText.text())

        movieModel.status = str(self.statusText.currentText())
        movieModel.spokenLanguage =str(self.spokenLanguageText.currentText())
        movieModel.storage =str(self.storageText.currentText())

        movieModel.comments = str(self.commentsText.toPlainText())
        
        return movieModel
               
    def cancel(self):
        self.clear();
        self.hide()                
    
    def clear(self):
        self.nameText.setText("")
        self.commentsText.setDocument(QtGui.QTextDocument(""))
        self.statusText.setCurrentIndex(0)
        self.spokenLanguageText.setCurrentIndex(0)
        self.storageText.setCurrentIndex(0)

        

class SaveButton(ui.DefaultComponents.SystemButton):
    
    def __init__(self, parentWidget):
        super(SaveButton, self).__init__(self, SAVE_BUTTON_LABEL)
        
        self.parentWidget = parentWidget
        self.connect(self, QtCore.SIGNAL('clicked()'), self.saveMovie)

    def saveMovie(self):
        if(self.text() == SAVE_BUTTON_LABEL):
            self.parentWidget.save()
        elif(self.text() == UPDATE_BUTTON_LABEL):
            self.parentWidget.update()

class CancelButton(ui.DefaultComponents.SystemButton):
    
    def __init__(self, parentWidget):
        super(CancelButton, self).__init__(self, " Cancel ")
        
        self.parentWidget = parentWidget
        self.connect(self, QtCore.SIGNAL('clicked()'), self.cancelAddMovieRequest)
    
    def cancelAddMovieRequest(self):
        self.parentWidget.cancel()
        
class PropertyComboBox(QtGui.QComboBox):
    
    def __init__(self, items):
        self.defaultItem = "-- Select --"
        
        super(PropertyComboBox, self).__init__()
        self.addItem(self.defaultItem)
        self.addItems(items)
        self.setStyleSheet("background :none;")
        self.setStyle(QtGui.QStyleFactory.create("macintos"));
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    def currentText(self):
        text = super(PropertyComboBox, self).currentText()
        
        if(self.defaultItem != text):
            return text
        else:
            return ""
    
    def updateCurrentIndexFor(self, itemText):
        index = self.findText(itemText)
        self.setCurrentIndex(index)


