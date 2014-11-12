# repository.py

# provides database interfce for domain objects

#import statements
import time
import sqlite3


from domainobjects import *
from core.IdGenerator import IdGenerator
###############################################################################
# Global Methods
def print_message(message, same_line = False):
    if same_line:
        print message + "",
    else:
        print "\n" + message + ""

###############################################################################        
#Wait class, defined to add a wait timer for few seconds.
class Wait:
    
    def __init__(self):
        self.defaultWaitTime = 1

    def run(self):
        for i in range(3):
            time.sleep(self.defaultWaitTime)

            print_message(".", same_line= True)

###############################################################################        
# Base class for all error.

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

###############################################################################        
# Error for database operations
class DatabaseError(Error):
    """Exception raised for errors during database operations.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg

###############################################################################
class Repository(object):

    def __init__(self):
        self.wait = Wait()
        print_message("Initializing Repository", same_line=True)
        self.wait.run()
        # Create a connection to the database.
        self.connection = sqlite3.connect("movies.db")
        self.connection.text_factory = str;
        

    def select(self, sqlstatement, parameters={}):
        # Create a cursor object, execute query and fetchall rows.
        cursor = self.connection.cursor()
        cursor.execute(sqlstatement, parameters)
        return cursor

    def insert_update(self, sqlstatement, parameters={}):
        # Create a cursor object, execute query and fetchall rows.
        cursor = self.connection.cursor()
        cursor.execute(sqlstatement, parameters)
        self.connection.commit();
        cursor.close();

    def destroy(self):
        # Commit any existing chagnes
        self.connection.commit()
        
        # close the connection
        self.connection.close()

        print_message("UserRepository Destroyed Successfully.")
        
    def isTableExists(self, tableName):
        
        sql_tablecheck = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + tableName + "'"
        cursor = self.select(sql_tablecheck)
        row = cursor.fetchone()
        if row != None and row[0] == tableName :
            return True
        else:
            return False

###############################################################################
class UserRepository(Repository):

    def __init__(self):
        super(UserRepository, self).__init__()

        # table name and query columns
        self.table_name = "user"
        self.id_column = "id"
        self.username_column = "username"
        
        if self.isTableExists(self.table_name) is True:
            print_message("User repository is initialized.")
        else:
            print_message("Creating user table.")
            #create user table
            createUserStatement = "create table user(id, username, password)"
            self.insert_update(createUserStatement)

            #Add Default users
            self.insert_update("insert into user(id, username, password) values ('1', 'admin','passed')")

            print_message("User table created. UserRepository Initialized.")
            self.wait.run()

    def find_user_by_id(self, userid):

        sql_query = self.create_select_query(self.table_name, self.id_column)
        
        cursor = self.select(sql_query , {"id" :str(userid)})

        row = cursor.fetchone()

        user = None   
        if row != None:
            user = self.bind_user(row)
        else:
            print_message("User not found for id : " + str(userid))
        return user

    def find_user_by_name(self, username):
        sql_query = self.create_select_query(self.table_name, self.username_column)

        cursor = self.insert_update(sql_query, {"username":str(username)})

        row = cursor.fetchone()

        user = None   
        if row != None:
            user = self.bind_user(row)
        else:
            print_message("User not found for username : " + str(username))
        return user

    def create_select_query(self, tablename, colname):

        sql_query = "SELECT * FROM " + str(tablename) + " WHERE "  + str(colname) + "=:" + str(colname)

        return sql_query
    
    def bind_user(self, row):
        userid = row[0]
        username = row[1]
        password = row[2]

        user = User(username, password)
        user._id = str(userid)
        
        return user
        
###############################################################################
class MovieRepository(Repository):

    def __init__(self):
        
        super(MovieRepository, self).__init__()
        
        # Table names and column names
        self.table_name = "movie"
        self.column_id = "movie_id"
        self.column_movie_name = "name"
        self.column_spoken_language = "spoken_language"
        self.column_status = "status"        
        self.column_storage_location = "storage_location"
        self.column_comments = "comments"

        self.idGenerator = IdGenerator()
                                
        if self.isTableExists(self.table_name) is True:
            print_message("Movie repository is initialized.")
        else:
            print_message("account table created. MovieRepository Initialized.")
            self.initialize_database()
            self.wait.run()

    def initialize_database(self):
        print_message("Creating movie table.")

        create_table_statement = """
                create table movie(
                        movie_id,
                        name,
                        spoken_language,
                        status,
                        storage_location,
                        comments)
                """    

        self.insert_update(create_table_statement)
        
    def save(self, movieModel):
    	#Verify: movie should not be duplicate in the database
        existing_movie = self.findMovieByName(movieModel.name)
    	# If valid : insert, Else Raise Error
        if(existing_movie == None):  
            sql_query = "insert into movie values ( :movie_id, :name, :spokenLanguage, :status, :storage, :comments)"
            #Generate id for the movie
            movieModel._id = self.idGenerator.generate()
    
            cursor = self.insert_update(sql_query, movieModel.toDictionary())
            
            print_message("Moive is added to database. Neme : " + str(movieModel.name))
        else:
            raise DatabaseError("An old record is found with name ==> "+ existing_movie.name)        

        return movieModel

    def findMovieByName(self, toFind):
        sql_query = "SELECT * FROM " +self.table_name+ " WHERE name =:name"

        cursor = self.select(sql_query, {"name" : str(toFind),})
        rows = cursor.fetchall()
        
        movieModel = None
        if(len(rows) <= 0):
            print_message("No Movie found with name : " + str(toFind))
        elif(len(rows) > 1):
            raise DatabaseError("Multiple Items found with the same name==> "+ toFind)
        else:
            movieModel = self.bind(rows[0])
            
        return movieModel

    def updateMovie(self, toUpdate):
        movie = self.database.update(toUpdate)

    def cleanup(self):
        self.database.deleteAll()

    def loadAllMovies(self):
        sql_query = "SELECT * FROM " + self.table_name +";"
        cursor = self.select(sql_query)
        movies = []
        for row in cursor.fetchall():
            mov = self.bind(row)
            movies.append(mov)
            
        return movies

    def bind(self, row):
        movieModel = MovieModel()
        movieModel._id, movieModel.name, movieModel.spokenLanguage, movieModel.status,movieModel.storage, movieModel.comments = row
        return movieModel        

    def findMatchingMovies(self, nameToSearch):
        sql_query = "SELECT * FROM " + self.table_name +" WHERE name LIKE '%" +nameToSearch+"%';"
        cursor = self.select(sql_query)
        movies = []
        for row in cursor.fetchall():
            mov = self.bind(row)
            movies.append(mov)
            
        return movies

