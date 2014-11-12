#domainobject.py
# Defines Domain objects.

import utils

is_empty = utils.StringUtils.is_empty

################################################################################

class ObjectIdentity(object):
    """
    Base class for all the domain objects in the system. It provides a unique
    id for all domain objects.
    """
    def __init__(self):
        self.id = 1

################################################################################    
class User(ObjectIdentity):
    """
    User object identifies a real user of the system. User is identified by
    username.

    Fields:
    username    ====>
    password    ====>
    id          ====>
    """
    def __init__(self, username, password):
        """
        Constructor, creates a new User object, from given user name and
        password parameters
        """

        super(User, self).__init__()
        
        self.username = str(username)
        self.password = str(password)

    def match_password(self, password):
        """
        Match the input password with the password from current user
        """
        matched = False

        if(self.password == password):
            matched = True

        return matched

        
################################################################################
# Represents a Movie.
#
class MovieModel:
    """
       Movie Model. Hold movie details 
    """
    def __init__(self, name="", spokenLanguage="", comments="", status="Unknown", storage="Not Identified"):
        self.name = name
        self.comments = comments
        self.status = status
        self.storage = storage
        self._id =""
        self.spokenLanguage= spokenLanguage
        
    def copyProperties(self, copyForm, copyTo):
        copyTo.name = copyForm.name
        copyTo.status = copyForm.status
        copyTo.storage = copyForm.storage
        copyTo.spokenLanguage = copyForm.spokenLanguage
        copyTo.comments = copyForm.comments
        
        return copyTo;
        
    def validate(self):
        """
            A valid MovieModel means, it has all the properties set in itself.
            All property should hold meaningful values. 
        """
        validationErrors = []
        stringutils = StringUtils()
        if not stringutils.isValid(self.name):
            validationErrors.append("Name is not valid")
        if not stringutils.isValid(self.comments):
            validationErrors.append("Commnets is not valid")
        if not stringutils.isValid(self.status):
            validationErrors.append("Status is not valid")
        if not stringutils.isValid(self.storage):
            validationErrors.append("Storage is not valid")
        if not stringutils.isValid(self.spokenLanguage):
            validationErrors.append("Spoken Language is not valid")

        
        return validationErrors
        
    def toDictionary(self, withid=True):
        dictionary = { 
                        'name': buffer(self.name), 
                        'comments': self.comments, 
                        'status': self.status,
                        'storage': self.storage,
                        'spokenLanguage': self.spokenLanguage
                    }
        
        if(withid):
            dictionary['movie_id'] = self._id
        
        return dictionary  
            
    def __str__(self):
        return str(self.toDictionary(True))

################################################################################
class  StringUtils:
    
    def isValid(self, inputText):
        return True

################################################################################        
class Document:
    
    def __init__(self, name, value):
        self.name = name
        
        self.value = value
        self.valueLowerCase = value.lowercase()
    
    def __str__(self):
        return {name : value, name+"_lc" : valueLowerCase}        

################################################################################
