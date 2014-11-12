from PyQt4 import QtGui, QtCore

import core.Constants as Constants

SYSTEM_BUTTON_STYLE =  "background :#62A9FF; \
                        border-radius: 10px;\
                        border:1px solid #282828 ;\
                        font: bold 12px;\
                        min-width: 50px;\
                        padding: 3px;"

SYSTEM_BUTTON_STYLE_PRESSED = "background :#62AFFF; \
                        border-radius: 10px;\
                        border:1px solid #282828 ;\
                        font: bold 12px;\
                        min-width: 50px;\
                        padding: 3px;"

class SystemButton(QtGui.QPushButton):
    
    def __init__(self, parentWidget, buttonText):
        super(SystemButton, self).__init__(buttonText)
        self.setStyleSheet(SYSTEM_BUTTON_STYLE)
        
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
    
    def mousePressEvent(self, event):
        self.setStyleSheet(SYSTEM_BUTTON_STYLE_PRESSED)
        
        super(SystemButton, self).mousePressEvent(event)
        
class SystemLabel(QtGui.QLabel):

    def __init__(self, parentWidget, labelText):
        super(SystemLabel, self).__init__(labelText)
        self.setStyleSheet(Constants.WIDGET_STYLE_NO_BORDER)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        
