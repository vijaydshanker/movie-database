#!/usr/bin/python
################################################################################
# Parser and undator from backend.

################################################################################
# Import Statements.
from core.repository import MovieRepository
from core.repository import DatabaseError
from core.domainobjects import *
from core.Constants import *

import os

################################################################################
class BackEndEntry:
    
    def __init__(self):
        print "Loading movies.........."
        self.movie_repositoy = MovieRepository()

    def doImport(self, location):
        
        if(os.path.exists(location)):
            print "Directory Exists."
            
            
            #load hindi movies
            self.load(location, "/hindi")
            
            #load english movie
            self.load(location, "/english")
        else:
            print "Directory Not Found : " + str(location)
    
    def load(self, location, language):
        
        #counter valiable.
        count = 0;
        
        movieLocation = location + language
        
        if(os.path.exists(movieLocation)):
            for root, dirs, files in os.walk(movieLocation):

                for f in files:
                    parts = os.path.splitext(f)
                    print "checking file ==> " + str(f)
                    
                    extention = parts[1]
                    if(self.isMovieFile(extention)):
                        movie = MovieModel()                                
                        movie.name = parts[0]
                        movie.status = Status.DOWNLOADED
                        movie.storage = Storage.MY_EXT_HARD_DISK
                        movie.comments = "Added by back end process."

                        if(language == "/hindi"):
                            movie.spokenLanguage = SpokenLanguage.HINDI

                        elif(language == "/english"):
                            movie.spokenLanguage = SpokenLanguage.ENGLISH
                        
                        try:
                            id = self.movie_repositoy.save(movie)
                            if id is not None:
                                print "Movie added successfully. "
                                count = count + 1;
                        except DatabaseError:
                            print "Movie not added."
                            
                        
                    else:
                        print str(f) + " is not a movie file."
                    
                    print ""                    
        else:
            print "Directory Not Found : " + str(movieLocation)
            
        print "Total Movies Addded to Database ==> " + str(count)


    def isMovieFile(self, extention):
        movieExtentions = [".avi", ".mkv", ".mp4", "divx"]
        
        for ext in movieExtentions:
            if(extention.lower() == ext.lower()):
                return True
    
BackEndEntry().doImport("/media/me/My Passport/me/Home/Videos")
        
