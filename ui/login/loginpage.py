################################################################################
# Import Statements.
import sys

from PyQt4 import QtGui, QtCore

from core.repository import UserRepository
from core.repository import Wait
from core.utils import StringUtils

from ui.home.homepage import MovieManager

################################################################################
# Global Declarations
is_empty = StringUtils.is_empty

################################################################################
# Constants define for login module.
LARGE_PRIME = 541
_KEY = 171  
MAX_FAILURES_ALLOWED = 3

repository = UserRepository()

################################################################################

# Global Methods
def show_message(message, same_line = False):
    if same_line:
        print message + "",
    else:
        print "\n" + message + ""

################################################################################
class LoginWindow(QtGui.QWidget):

    def __init__(self):
        self.root = QtGui.QApplication(sys.argv)
        super(LoginWindow, self).__init__()
        
        # Set Basic window properties
        self.setWindowTitle("Authentication Point.")
        self.setGeometry(350, 350, 400, 70)
        
        #Pages for login Request
        self.login_id_checkpoint = LoginIdCheckPoint(self)
        self.authentication_check_point = AuthenticationCheckPoint(self)
        self.home_page = MovieManager()

        # layout        
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        
        #service point for login requests
        self.check_point = IdentityCheckPoint();

    def identify_user(self, userid):
        status_passed = self.check_point.do_check(userid)
        
        if status_passed:
            # save user info
            self.login_actor = userid
            
            #remove first page
            self.login_id_checkpoint.hide()
            
            #add authentication token page
            self.add(self.authentication_check_point)
        else:
            QtGui.QMessageBox.information(self, "Info",
                userid + " is not a valid user id.")

    def verify_password(self, password):
        status_passed = self.check_point.verify_password(self.login_actor, password)
        
        if status_passed:
            #remove login window and show home page
            self.hide()
            
            self.home_page.show_view()
        else:
            print "User not identified"

    def add(self, widget):
        # add default login page.
        self.layout.addWidget(widget)
                    
    def showView(self):
        self.add(self.login_id_checkpoint)
        
        self.show()
        sys.exit(self.root.exec_())
        
        
        
################################################################################
class LoginIdCheckPoint(QtGui.QFrame):
    """
    Default page for process. Recieves ID of the user to login.
    """
    
    def __init__(self, parent):
        super(LoginIdCheckPoint, self).__init__()

        self.login_window = parent 
        
        self.initUI()
        
        
    def initUI(self):
        self.main_content = QtGui.QFrame(self)
        
        layout = QtGui.QHBoxLayout()

        self.user_id_label = QtGui.QLabel("Please Enter your User Id ")
        self.user_id_label.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed)

        self.input_box = QtGui.QLineEdit()
        self.input_box.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                     QtGui.QSizePolicy.Fixed)
        self.input_box.setFocus()

        self.go_button = QtGui.QPushButton(" Go ", self)
        self.go_button.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                     QtGui.QSizePolicy.Fixed)
        
        #action added to go button
        self.connect(self.go_button, QtCore.SIGNAL("clicked()"),
                     self.go_button_clicked)

        layout.addWidget(self.user_id_label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.go_button)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(layout)

        self.main_content.setLayout(main_layout)

    def go_button_clicked(self):
    
        userid = self.input_box.text()
        
        if is_empty(userid):
            QtGui.QMessageBox.information(self, "Info",
                "Please, Enter a valid user id.")
        else:
            self.login_window.identify_user(userid)
                        
################################################################################
# Next  step after user id is verified.
class AuthenticationCheckPoint(QtGui.QFrame):

    def __init__(self, parent):
        super(AuthenticationCheckPoint,self).__init__()
        
        self.login_window = parent 
        
        self.init_gui()
        
    def init_gui(self):
        layout = QtGui.QHBoxLayout()

        label = QtGui.QLabel("Please enter your Password")
        label.setSizePolicy(QtGui.QSizePolicy.Fixed,
                            QtGui.QSizePolicy.Fixed)

        self.password_box = QtGui.QLineEdit()
        self.password_box.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                        QtGui.QSizePolicy.Fixed)
        self.password_box.setEchoMode(QtGui.QLineEdit.Password)
                                        
        self.password_box.setFocus()
        
        self.submit_button = QtGui.QPushButton(" Submit ")
        self.submit_button.setSizePolicy(QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed)
        #action with submit button
        self.connect(self.submit_button, QtCore.SIGNAL("clicked()"),
                     self.submit_button_clicked)

        layout.addWidget(label)
        layout.addWidget(self.password_box)
        layout.addWidget(self.submit_button)

        main_content = QtGui.QFrame(self)
        
        main_content.setLayout(layout)
        
    def submit_button_clicked(self):
        
        password = self.password_box.text()
        
        self.login_window.verify_password(password)


################################################################################
# Login Class
class IdentityCheckPoint:

    def __init__(self):
        show_message("Initializing checkpoint", same_line=True)
        self.wait = Wait()
        self.wait.run()

    def do_check(self, idnumber):
        #get username for the id number
        user = repository.find_user_by_id(idnumber)
        
        status =  False
        if(user == None):
            status = False
        else:
            status = True
            
        return status    

    def verify_password(self, userid, password):
    
        #get username for the id number
        user = repository.find_user_by_id(userid)
        
        is_valid = False
        
        if user.match_password(password):
            is_valid = True
        else:
            pass
        
        return is_valid
                
